# Existing imports
from flask import Response
from datetime import datetime

# Custom imports
import SignatureClassifier.classifier_interface as classifier_interface
import SignatureClassifier.signature_detection as signature
from JWT.jwt import JWT

def before_request(request, session):
    # Firewall Logic
    # You can use the request.headers, request.method, request.path, etc. to make decisions
    
    # Rule-based detection
    print("Rule-based detection:")

    # Block requests from a specific IP address
    # if request.remote_addr == '127.0.0.1':    
    #     logger(f'Blocked request from IP address: {request.remote_addr}')
    #     return 'Access denied', 403

    # Block requests to a specific path
    # if request.path == '/private':
    #     logger(f'Blocked request to path: {request.path} from IP address: {request.remote_addr}')
    #     return 'Access denied', 403

    # Block requests with a specific user agent
    # if 'User-Agent' in request.headers and 'bad_agent' in request.headers['User-Agent']:
    #     logger(f'Blocked request with bad user agent: {request.headers["User-Agent"]} from IP address: {request.remote_addr}')
    #     return 'Access denied', 403
    
    # Block requests with a anomalous token
    if check_token(session.cookies):
        return 'Access denied', 403
    
    # Signature-based detection
    print("Signature-based detection:")

    # Block requests with an anomalous signature
    if check_signature_detection(session.cookies):
        return 'Access denied', 403
    
    # Anomaly-based detection
    print("Anomaly-based detection:")

    # Block requests with an anomalous pattern
    if check_anomaly_detection(session.cookies, request):
        return 'Access denied', 403

    # If none of the conditions match, allow the request to proceed
    return None

def proxy(path, SITE_NAME, request, session):
    if request.method=='GET':
        resp = session.get(f'{SITE_NAME}{path}', headers=dict(request.headers))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='POST':
        resp = session.post(f'{SITE_NAME}{path}', data=request.form, headers=dict(request.headers))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response

def check_token(session_requests_cookies):
    if session_requests_cookies:
        for cookie in session_requests_cookies:
            if cookie.name == "token":
                jwttoken = cookie.value # extract the jwt token string
                header = JWT.get_unverified_header(jwttoken) # get the jwt token header, figure out which algorithm the web server is using
                payload = JWT._base64url_decode(jwttoken, options={"verify_signature": False}) # decode the jwo token payload, the user role information is claimed in the payload
                if payload['role'] == 'admin' and header['alg'] == 'none': # check if the user role is admin and the algorithm is HS256
                    return False
    return True

def check_signature_detection(session_requests_cookies, request):
    # Load the signature detection module
    classification = signature.signature_detection(request.method + ' ' + request.path + ' ' + request.data + ' ' + request.query_string)

    # Check for anomalies using the signature detection module
    if classification == 'Anomalous':
        logger(f'Anomalous signature: {request.method} {request.path} {request.data} {request.query_string}')
        return True
    logger(f'Non-anomalous signature: {request.method} {request.path} {request.data} {request.query_string}')
    return False

def check_anomaly_detection(session_requests_cookies, request):
    # Load the baseline trainer
    classification = classifier_interface.classify(request.method + ' ' + request.path + ' ' + request.data + ' ' + request.query_string)

    # Check for anomalies using the baseline trainer
    if classification == 'Anomalous':
        logger(f'Anomalous request: {request.method} {request.path} {request.data} {request.query_string}')
        return True
    logger(f'Non-anomalous request: {request.method} {request.path} {request.data} {request.query_string}')
    return False

def logger(message):
    with open('log.txt', 'a') as f:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'{current_time} - {message}\n')