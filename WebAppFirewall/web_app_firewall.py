from flask import Response
import requests, jwt
import re
import datetime
import http_dataset.baseline_trainer as baseline_trainer

def before_request(request):
    # Firewall Logic
    # You can use the request.headers, request.method, request.path, etc. to make decisions

    # Block requests from a specific IP address
    if request.remote_addr == '127.0.0.1':
        logger(f'Blocked request from IP address: {request.remote_addr}')
        return 'Access denied', 403

    # Block requests to a specific path
    if request.path == '/private':
        logger(f'Blocked request to path: {request.path} from IP address: {request.remote_addr}')
        return 'Access denied', 403

    # Block requests with a specific user agent
    if 'User-Agent' in request.headers and 'bad_agent' in request.headers['User-Agent']:
        logger(f'Blocked request with bad user agent: {request.headers["User-Agent"]} from IP address: {request.remote_addr}')
        return 'Access denied', 403
    
    # Block requests with a specific cookie
    if check_token(requests.session().cookies):
        return 'Access denied', 403

    # If none of the conditions match, allow the request to proceed
    return None

def proxy(path, SITE_NAME, request):
    if request.method=='GET':
        resp = requests.session().get(f'{SITE_NAME}{path}', headers=dict(request.headers))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='POST':
        resp = requests.session().post(f'{SITE_NAME}{path}', data=request.form, headers=dict(request.headers))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response

def check_token(session_requests_cookies):
    if session_requests_cookies:
        for cookie in session_requests_cookies:
            if cookie.name == "token":
                jwttoken = cookie.value # extract the jwt token string
                header = jwt.get_unverified_header(jwttoken) # get the jwt token header, figure out which algorithm the web server is using
                payload = jwt.decode(jwttoken, options={"verify_signature": False}) # decode the jwo token payload, the user role information is claimed in the payload
                if payload['role'] == 'admin' and header['alg'] == 'none': # check if the user role is admin and the algorithm is HS256
                    return False
    return True

def check_signature_detection(session_requests_cookies):
    # Test for SQL Injection
    rules = [ # Signature-based detection rules
        # SQL Injection
        'delete from users', 'select * from users', 'delete,from', 'select,from', 'drop,table', 'union,select', 'update,set'
        # XSS
        '&cmd', 'exec', 'concat', '../', '</script>'
        # Command Injection
        '&&', '|', '||', '&&', ';', '||', '`', '$', '(', ')', '{', '}', '[', ']', '==', '!=', '>', '<', '>=', '<=', 'eq', 'ne', 'gt', 'lt', 'ge', 'le'
    ]

    for cookie in session_requests_cookies:
        for rule in rules:
            if re.search(rule, cookie.value, re.I):
                return True
            return False

def check_anomaly_detection(session_requests_cookies, request):
    # Load the baseline trainer

    # Initialize the baseline trainer
    trainer = baseline_trainer.BaselineTrainer()

    # Get the request data
    request_data = {
        'method': request.method,
        'path': request.path,
        'headers': dict(request.headers),
        'cookies': session_requests_cookies
    }

    # Check for anomalies using the baseline trainer
    if trainer == True:
        return True
    return False

def logger(message):
    with open('log.txt', 'a') as f:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'{current_time} - {message}\n')