# Existing imports
from flask import Response
from datetime import datetime
import sys

# Custom imports
sys.path.append("WebAppFirewall/Classifier/Classifier/")
import Classifier.Classifiers.classifier_interface as classifier_interface
from Classifier.Classifiers.count_vectorizer import SimpleCountVectorizer
from Classifier.Classifiers.classifier import OneClassSVMClassifier, MultinomialNaiveBayes
from JWT.jwt import JWT

def before_request(request, session, settings, rules):
    # print("Before request:")
    # Firewall Logic
    
    # Rule-based detection
    # print("Rule-based detection:")

    # Block requests from a specific IP address
    if check_rules(request, settings['rule_settings'], rules):
        return 'Access denied', 403
    
    # Block requests with a anomalous token
    if check_token(session.cookies, settings['token_settings']):
        return 'Access denied', 403
    
    # Signature-based detection
    # print("Signature-based detection:")

    # Block requests with an anomalous signature
    if check_signature_detection(request, settings['signature_settings']):
        return 'Access denied', 403
    
    # Anomaly-based detection
    # print("Anomaly-based detection:")

    # Block requests with an anomalous pattern
    if check_anomaly_detection(session.cookies, request, settings['anomaly_settings']):
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
    if self_time > self_rtt:
        logger(f'Request took longer than expected: {self_time*1000} vs {self_rtt*1000}')
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
    # print("Check token:")
    if token_settings['check_token'] and session_requests_cookies:
        for cookie in session_requests_cookies:
            if cookie.name == "token":
                jwttoken = cookie.value # extract the jwt token string
                header = JWT.get_unverified_header(jwttoken) # get the jwt token header, figure out which algorithm the web server is using
                payload = JWT._base64url_decode(jwttoken, options={"verify_signature": False}) # decode the jwo token payload, the user role information is claimed in the payload
                if payload['role'] == 'admin' and header['alg'] == 'none': # check if the user role is admin and the algorithm is HS256
                    logger(f'Blocked token: {jwttoken}')
                    return True
                logger(f'Allowed token: {jwttoken}')
    return False

def check_signature_detection(request, signature_settings):
    # print("Check signature detection:")
    if signature_settings['check_signature']:
        # Load the signature detection module
        classification = classifier_interface.classify(request.method + ' ' + request.path + ' ' + request.data.decode("utf-8") + ' ' + request.query_string.decode("utf-8"), classifier_type='mnb', dataset='csic')

        # Check for anomalies using the signature detection module
        if classification == 'Anomalous':
            logger(f'Anomalous signature: {request.method} {request.path} {request.data} {request.query_string}')
            return True
        logger(f'Non-anomalous signature: {request.method} {request.path} {request.data} {request.query_string}')
    return False

def check_anomaly_detection(session_requests_cookies, request, anomaly_settings):
    # print("Check anomaly detection:")
    classification = None
    if anomaly_settings['check_anomaly']:
        # Load the baseline trainer
        if session_requests_cookies:
            for cookie in session_requests_cookies:
                if cookie.name == "token":
                    jwttoken = cookie.value # extract the jwt token string
                    header = JWT.get_unverified_header(jwttoken) # get the jwt token header, figure out which algorithm the web server is using
                    payload = JWT._base64url_decode(jwttoken, options={"verify_signature": False}) # decode the jwo token payload, the user role information is claimed in the payload
                    classification = classifier_interface.classify(request.path + ' ' + request.method, classifier_type='svm', dataset='ctf')
        else:
            # classification = classifier_interface.classify(request.path + ' ' + request.method + ' ' + payload['role'] + ' ' + header['alg'], classifier_type='svm', dataset='ctf')
            classification = classifier_interface.classify(request.path + ' ' + request.method, classifier_type='svm', dataset='ctf')
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

def log_time(self_time, self_rtt):
    with open('time.txt', 'a') as f:
        f.write(f'{self_time}, {self_rtt}\n')