# Existing imports
from flask import Response
from datetime import datetime
import sys

# Custom imports
sys.path.append("WebAppFirewall/Classifier/Classifiers/")
import Classifier.Classifiers.classifier_interface as classifier_interface
from JWT.jwt import JWT

def before_request(request, session, settings, rules, container_name):
    # Firewall Logic

    # Block requests from a specific IP address
    if check_rules(request, settings, rules):
        return 'Access denied', 403
    
    # Block requests with a anomalous token
    if check_token(session.cookies, settings):
        return 'Access denied', 403

    # Block requests with an anomalous signature
    if check_signature_detection(request, settings):
        return 'Access denied', 403

    # Block requests with an anomalous pattern
    if check_anomaly_detection(session.cookies, request, settings, container_name):
        return 'Access denied', 403

    # If none of the conditions match, allow the request to proceed
    return None

def proxy(path, SITE_NAME, request, session):
    # print("Proxy:")
    if request.method=='GET':
        resp = session.get(f'{SITE_NAME}{path}', headers=dict(request.headers))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
    elif request.method=='POST':
        resp = session.post(f'{SITE_NAME}{path}', data=request.form, headers=dict(request.headers))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
    return response, resp.elapsed.total_seconds()
    
def post_request(request, self_time, self_rtt):
    log_time(self_time*1000, self_rtt*1000)
    # if self_time > self_rtt:
        # logger(f'Request took longer than expected: {self_time*1000} vs {self_rtt*1000}')
    # print("Post request:")
    with open('requests.txt', 'a') as f:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'{current_time} - {request.method} {request.path}\n')

def check_rules(request, rule_settings, rules):
    # print("Check rules:")
    # Block requests from a specific IP address
    if rule_settings['block_remote_addr'] and request.remote_addr not in rules['blocked_ips']:
        logger(f'Blocked IP: {request.remote_addr}')
        return True
    
    # Block requests with a specific User-Agent header
    if rule_settings['block_user_agent'] and request.headers.get('User-Agent') not in rules['blocked_user_agents']:
        logger(f'Blocked User-Agent: {request.headers.get("User-Agent")}')
        return True
    
    # Block requests to specific paths
    if rule_settings['block_path'] and request.path not in rules['blocked_paths']:
        logger(f'Blocked path: {request.path}')
        return True
    
    # Block requests with specific query strings
    if rule_settings['block_query_string'] and request.query_string not in rules['blocked_query_strings']:
        logger(f'Blocked query string: {request.query_string}')
        return True

    return False

def check_token(session_requests_cookies, token_settings):
    if token_settings['check_token'] and session_requests_cookies:
        print("Check token:")
        for cookie in session_requests_cookies:
            if cookie.name == "token":
                jwttoken = cookie.value # extract the jwt token string
                header = JWT.get_unverified_header(jwttoken) # get the jwt token header, figure out which algorithm the web server is using
                payload = JWT.decode(jwttoken, options={"verify_signature": False}) # decode the jwo token payload, the user role information is claimed in the payload
                if payload['role'] == 'admin' and header['alg'] == 'none': # check if the user role is admin and the algorithm is HS256
                    logger(f'Blocked token: {jwttoken}')
                    return True
                logger(f'Allowed token: {jwttoken}')
    return False

def check_signature_detection(request, signature_settings):
    if signature_settings['check_signature']:
        print("Check signature detection:")
        # Load the signature detection module
        classification = ""
        get_query = ""
        post_data = ""
        if request.method == 'GET':
            get_query = request.query_string.decode('utf-8')
            if get_query == "":
                get_query = "None"
            else:
                get_query = get_query[10:]
            classification = classifier_interface.classify(request.method + ' ' + request.path + ' ' + get_query, classifier_type='mnb', dataset='csic')
        elif request.method == 'POST':
            post_data = request.form.get('post-data')
            if post_data == None:
                post_data = ""
            classification = classifier_interface.classify(request.method + ' ' + request.path + ' ' + post_data, classifier_type='mnb', dataset='csic')
        
        # Check for anomalies using the signature detection module
        if classification == 'Anomalous':
            logger(f'Anomalous signature: {request.method} {request.path} {post_data} {get_query}')
            return True
        logger(f'Non-anomalous signature: {request.method} {request.path} {post_data} {get_query}')
    return False

def check_anomaly_detection(session_requests_cookies, request, anomaly_settings, container_name):
    if anomaly_settings['check_anomaly']:
        print("Check anomaly detection:")
        # Load the baseline trainer
        classification = ""
        jwttoken = ""
        get_query = request.query_string.decode('utf-8')
        if container_name == 'CTF_WAF':
            classification = classifier_interface.classify(request.path + get_query + ' ' + request.method, classifier_type='svm', dataset='ctf')
        elif container_name == 'TIREDFUL_WAF':
            if session_requests_cookies:
                for cookie in session_requests_cookies:
                    if cookie.name == "token":
                        jwttoken = cookie.value # extract the jwt token string
                        header = JWT.get_unverified_header(jwttoken) # get the jwt token header, figure out which algorithm the web server is using
                        payload = JWT._base64url_decode(jwttoken, options={"verify_signature": False}) # decode the jwo token payload, the user role information is claimed in the payload
                        classification = classifier_interface.classify(request.path + get_query + ' ' + payload['role'] + ' ' + request.method, classifier_type='svm', dataset='tiredful')
            else:
                classification = classifier_interface.classify(request.path + get_query + ' ' + request.method, classifier_type='svm', dataset='tiredful')
        elif container_name == 'DVWA_WAF':
            classification = classifier_interface.classify(request.path + get_query, classifier_type='svm', dataset='dvwa')

        # Check for anomalies using the baseline trainer
        if classification == 'Anomalous':
            logger(f'Anomalous behaviour: {request.method} {request.path}{get_query} {jwttoken}')
            return True
        logger(f'Non-anomalous behaviour: {request.method} {request.path}{get_query} {jwttoken}')
    return False

def logger(message):
    with open('log.txt', 'a') as f:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'{current_time} - {message}\n')

def log_time(self_time, self_rtt):
    with open('time.txt', 'a') as f:
        f.write(f'{self_time}, {self_rtt}\n')