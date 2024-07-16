from flask import Flask, request

app = Flask(__name__)

@app.before_request
def web_app_firewall():
    # Implement your firewall logic here
    # You can access the request object to inspect the incoming request
    # You can use the request.headers, request.method, request.path, etc. to make decisions

    # Example: Block requests from a specific IP address
    if request.remote_addr == '127.0.0.1':
        return 'Access denied', 403

    # Example: Block requests to a specific path
    if request.path == '/admin':
        return 'Access denied', 403

    # Example: Block requests with a specific user agent
    if 'User-Agent' in request.headers and 'bad_agent' in request.headers['User-Agent']:
        return 'Access denied', 403

    # If none of the conditions match, allow the request to proceed
    return None

# Your application routes go here
@app.route('/')
def index():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run()
