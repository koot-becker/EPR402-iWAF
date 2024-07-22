from flask import Flask,request,redirect,Response
import requests
app = Flask(__name__)
SITE_NAME = 'http://192.168.8.22:8080/'

@app.before_request
def web_app_firewall():
    # Implement your firewall logic here
    # You can access the request object to inspect the incoming request
    # You can use the request.headers, request.method, request.path, etc. to make decisions

    # Example: Block requests from a specific IP address
    if request.remote_addr == '127.0.0.1':
        return 'Access denied', 403

    # Example: Block requests to a specific path
    if request.path == '/private':
        return 'Access denied', 403

    # Example: Block requests with a specific user agent
    if 'User-Agent' in request.headers and 'bad_agent' in request.headers['User-Agent']:
        return 'Access denied', 403

    # If none of the conditions match, allow the request to proceed
    return None

@app.route('/<path:path>',methods=['GET','POST',"DELETE"])
def proxy(path):
    global SITE_NAME
    if request.method=='GET':
        resp = requests.get(f'{SITE_NAME}{path}')
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='POST':
        resp = requests.post(f'{SITE_NAME}{path}',json=request.get_json())
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=='DELETE':
        resp = requests.delete(f'{SITE_NAME}{path}').content
        response = Response(resp.content, resp.status_code, headers)
        return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = False, port=5000)