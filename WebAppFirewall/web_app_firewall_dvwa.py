# Existing imports
from flask import Flask,request
from requests import session

# Custom imports
import web_app_firewall

# Global variables
dvwa_waf = Flask(__name__)
DVWA_SITE_NAME = 'http://127.0.0.1:8002/'

@dvwa_waf.before_request
def before_request():
    return web_app_firewall.before_request(request, session())

@dvwa_waf.after_request
def after_request(response):
    web_app_firewall.post_request(request)
    return response

@dvwa_waf.route('/')
def home():
    global DVWA_SITE_NAME
    return web_app_firewall.proxy('/', DVWA_SITE_NAME, request, session())

@dvwa_waf.route('/<path:path>',methods=['GET','POST'])
def proxy(path):
    global DVWA_SITE_NAME
    return web_app_firewall.proxy(path, DVWA_SITE_NAME, request, session())

if __name__ == '__main__':
    dvwa_waf.run(host='0.0.0.0', debug = False, port=5002)