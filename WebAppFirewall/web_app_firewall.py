from flask import Flask,request,redirect,Response,session
import requests, jwt
import re
import base64
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import datetime
app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
SITE_NAME = 'http://127.0.0.1:8001/'

@app.before_request
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

@app.route('/',methods=['GET','POST',"DELETE"])
def home():
    global SITE_NAME
    if request.method=='GET':
        resp = requests.session().get(f'{SITE_NAME}')
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        if check_token(requests.session().cookies):
            return response
        else:
            logger(f'Blocked request to path: {request.path} from IP address: {request.remote_addr} due to invalid token')
            return 'Access denied', 403

    elif request.method=='POST':
        resp = requests.post(f'{SITE_NAME}', data=request.form, headers=dict(request.headers))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response

@app.route('/<path:path>',methods=['GET','POST',"DELETE"])
def proxy(path):
    global SITE_NAME
    if request.method=='GET':
        resp = requests.session().get(f'{SITE_NAME}{path}')
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        if check_token(requests.session().cookies):
            return response
        else:
            logger(f'Blocked request to path: {request.path} from IP address: {request.remote_addr} due to invalid token')
            return 'Access denied', 403
    elif request.method=='POST':
        resp = requests.post(f'{SITE_NAME}{path}', data=request.form, headers=dict(request.headers))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response

# @app.after_request
# def after_request(response):
#     if check_token(session_requests.cookies):
#         if check_signature_detection(session_requests.cookies):
#             logger(f'Blocked request to path: {request.path} from IP address: {request.remote_addr} due to signature detection')
#             return 'Access denied', 403
#         if check_anomaly_detection(session_requests.cookies):
#             return 'Access denied', 403

def check_token(session_requests_cookies):
    for cookie in session_requests_cookies:
        if cookie.name == "token":
            jwttoken = cookie.value # extract the jwt token string
            header = jwt.get_unverified_header(jwttoken) # get the jwt token header, figure out which algorithm the web server is using
            payload = jwt.decode(jwttoken, options={"verify_signature": False}) # decode the jwo token payload, the user role information is claimed in the payload
            if payload['role'] == 'admin':
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

def decode(jwt_string):
    return base64.b64decode(jwt_string + '===').decode('utf-8')

def encode(jwt_string):
    return base64.b64encode(jwt_string.encode()).decode('utf-8').rstrip('=')

def logger(message):
    with open('log.txt', 'a') as f:
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f'{current_time} - {message}\n')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True, port=5000)