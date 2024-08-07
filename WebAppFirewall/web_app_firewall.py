from flask import Flask,request,redirect,Response,session
import requests, jwt
import re
import base64
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import datetime
ctf_waf = Flask(__name__)
tiredful_waf = Flask(__name__)
dvwa_waf = Flask(__name__)
TIREDFUL_SITE_NAME = 'http://127.0.0.1:8000/'
CTF_SITE_NAME = 'http://127.0.0.1:8001/'
DVWA_SITE_NAME = 'http://127.0.0.1:8002/'

@ctf_waf.before_request
@tiredful_waf.before_request
@dvwa_waf.before_request
def before_request():
    # Implement your firewall logic here
    # You can access the request object to inspect the incoming request
    # You can use the request.headers, request.method, request.path, etc. to make decisions

    # Example: Block requests from a specific IP address
    # if request.remote_addr == '127.0.0.1':
    #     logger(f'Blocked request from IP address: {request.remote_addr}')
    #     return 'Access denied', 403

    # Example: Block requests to a specific path
    # if request.path == '/private':
    #     logger(f'Blocked request to path: {request.path} from IP address: {request.remote_addr}')
    #     return 'Access denied', 403

    # Example: Block requests with a specific user agent
    # if 'User-Agent' in request.headers and 'bad_agent' in request.headers['User-Agent']:
    #     logger(f'Blocked request with bad user agent: {request.headers["User-Agent"]} from IP address: {request.remote_addr}')
    #     return 'Access denied', 403

    # If none of the conditions match, allow the request to proceed
    return None

@ctf_waf.route('/')
@tiredful_waf.route('/')
@dvwa_waf.route('/')
def home():
    global CTF_SITE_NAME
    if request.method=='GET':
        resp = requests.session().get(CTF_SITE_NAME)
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        if check_token(requests.session().cookies):
            return response
        else:
            logger(f'Blocked request to path: {request.path} from IP address: {request.remote_addr} due to invalid token')
            return 'Access denied', 403
    elif request.method=='POST':
        resp = requests.session().post(CTF_SITE_NAME, data=request.form, headers=dict(request.headers))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        if check_token(requests.session().cookies):
            return response
        else:
            logger(f'Blocked request to path: {request.path} from IP address: {request.remote_addr} due to invalid token')
            return 'Access denied', 403

@ctf_waf.route('/<path:path>',methods=['GET','POST'])
@tiredful_waf.route('/<path:path>',methods=['GET','POST'])
@dvwa_waf.route('/<path:path>',methods=['GET','POST'])
def proxy(path):
    global CTF_SITE_NAME
    if request.method=='GET':
        resp = requests.session().get(f'{CTF_SITE_NAME}{path}')
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        if check_token(requests.session().cookies):
            return response
        else:
            logger(f'Blocked request to path: {request.path} from IP address: {request.remote_addr} due to invalid token')
            return 'Access denied', 403
    elif request.method=='POST':
        resp = requests.session().post(f'{CTF_SITE_NAME}{path}', data=request.form, headers=dict(request.headers))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        if check_token(requests.session().cookies):
            return response
        else:
            logger(f'Blocked request to path: {request.path} from IP address: {request.remote_addr} due to invalid token')
            return 'Access denied', 403

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

def check_anomaly_detection(session_requests_cookies):
    # Load historical data from log file
    with open('log.txt', 'r') as f:
        data = f.readlines()

    # Prepare the data for training
    X = []
    y = []
    for line in data:
        if 'Blocked' in line:
            X.append(line)
            y.append(1)  # Anomaly
        else:
            X.append(line)
            y.append(0)  # Normal

    # Vectorize the text data
    vectorizer = CountVectorizer()
    X_vectorized = vectorizer.fit_transform(X)

    # Train the Naive Bayes classifier
    classifier = MultinomialNB()
    classifier.fit(X_vectorized, y)

    # Classify the current request
    current_request = f'Request from IP address: {request.remote_addr} to path: {request.path}'
    current_request_vectorized = vectorizer.transform([current_request])
    prediction = classifier.predict(current_request_vectorized)

    # Return the result
    if prediction[0] == 1:
        logger(f'Anomaly detected: {current_request}')
        return 'Access denied', 403
    else:
        return None

def logger(message):
    with open('log.txt', 'a') as f:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'{current_time} - {message}\n')

if __name__ == '__main__':
    ctf_waf.run(host='0.0.0.0', debug = False, port=5000)
    # tiredful_waf.run(host='0.0.0.0', debug = False, port=5001)
    # dvwa_waf.run(host='0.0.0.0', debug = False, port=5002)