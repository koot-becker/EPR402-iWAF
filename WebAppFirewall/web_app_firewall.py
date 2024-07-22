from flask import Flask,request,redirect,Response
import requests, jwt
import base64
app = Flask(__name__)
SITE_NAME = 'http://192.168.8.22:8080/'

@app.before_request
def web_app_firewall():
    # Implement your firewall logic here
    # You can access the request object to inspect the incoming request
    # You can use the request.headers, request.method, request.path, etc. to make decisions

    # Example: Block requests from a specific IP address
    if request.remote_addr == '127.0.0.1':
        logger(f'Blocked request from IP address: {request.remote_addr}')
        return 'Access denied', 403

    # Example: Block requests to a specific path
    if request.path == '/private':
        logger(f'Blocked request to path: {request.path} from IP address: {request.remote_addr}')
        return 'Access denied', 403

    # Example: Block requests with a specific user agent
    if 'User-Agent' in request.headers and 'bad_agent' in request.headers['User-Agent']:
        logger(f'Blocked request with bad user agent: {request.headers["User-Agent"]} from IP address: {request.remote_addr}')
        return 'Access denied', 403
    
    # Check JWT token validity
    if 'Authorization' in request.headers:
        token = request.headers['Authorization'].split(' ')[1]
        header, payload, signature = token.split('.')
        decoded_payload = decode(payload)
        if 'admin' in decoded_payload:
            logger(f'Blocked request with admin token: {token} from IP address: {request.remote_addr}')
            return 'Access denied', 403
        
    # Check for SQL Injection
    if 'sql' in request.args:
        logger(f'Blocked request with SQL Injection: {request.url} from IP address: {request.remote_addr}')
        return 'Access denied', 403
    
    # Check for XSS
    if 'xss' in request.args:
        logger(f'Blocked request with XSS: {request.url} from IP address: {request.remote_addr}')
        return 'Access denied', 403
    
    # Check for CSRF
    if 'csrf' in request.args:
        logger(f'Blocked request with CSRF: {request.url} from IP address: {request.remote_addr}')
        return 'Access denied', 403
    
    # Check for Path Traversal
    if 'path' in request.args:
        logger(f'Blocked request with Path Traversal: {request.url} from IP address: {request.remote_addr}')
        return 'Access denied', 403
    
    # Check for Command Injection
    if 'cmd' in request.args:
        logger(f'Blocked request with Command Injection: {request.url} from IP address: {request.remote_addr}')
        return 'Access denied', 403
    
    # Check for LFI
    if 'lfi' in request.args:
        logger(f'Blocked request with LFI: {request.url} from IP address: {request.remote_addr}')
        return 'Access denied', 403

    # If none of the conditions match, allow the request to proceed
    return None

@app.route('/<path:path>',methods=['GET','POST',"DELETE"])
def proxy(path):
    global SITE_NAME
    global session_requests
    if request.method=='GET':
        resp = requests.get(f'{SITE_NAME}{path}')
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='POST':
        resp = session_requests.post(f'{SITE_NAME}{path}', data=request.form, headers=dict(request.headers))
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        if check_token(session_requests.cookies):
            return response
        else:
            return 'Access denied', 403
    elif request.method=='DELETE':
        resp = requests.delete(f'{SITE_NAME}{path}').content
        response = Response(resp.content, resp.status_code, headers)
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False, port=5000)

def decode(jwt_string):
    return base64.b64decode(jwt_string + '===').decode('utf-8')

def encode(jwt_string):
    return base64.b64encode(jwt_string.encode()).decode('utf-8').rstrip('=')

def logger(message):
    with open('log.txt', 'a') as f:
        f.write(message + '\n')

    
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
    sql_injection = ('delete from users', 'select * from users', 'delete,from', 'select,from', 'drop,table', 'union,select', {'update,set'})
    xss = ('&cmd', 'exec', 'concat', '../', '</script>')