# Existing imports
from flask import Flask,request
from requests import session

# Custom imports
import web_app_firewall

# Global variables
tiredful_waf = Flask(__name__)
TIREDFUL_SITE_NAME = 'http://127.0.0.1:8000/'

@tiredful_waf.before_request
def before_request():
    return web_app_firewall.before_request(request, session())

@tiredful_waf.after_request
def after_request(response):
    web_app_firewall.post_request(request)
    return response

@tiredful_waf.route('/')
def home():
    global TIREDFUL_SITE_NAME
    return web_app_firewall.proxy('/', TIREDFUL_SITE_NAME, request, session())

@tiredful_waf.route('/<path:path>',methods=['GET','POST'])
def proxy(path):
    global TIREDFUL_SITE_NAME
    return web_app_firewall.proxy(path, TIREDFUL_SITE_NAME, request, session())

if __name__ == '__main__':
    tiredful_waf.run(host='0.0.0.0', debug = False, port=5000)