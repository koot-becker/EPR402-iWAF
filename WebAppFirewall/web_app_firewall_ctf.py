# Existing imports
from flask import Flask,request,Response
from requests import session

# Custom imports
import web_app_firewall

# Global variables
ctf_waf = Flask(__name__)
CTF_SITE_NAME = 'http://127.0.0.1:8001/'

@ctf_waf.before_request
def before_request():
    web_app_firewall.before_request(request, session())

@ctf_waf.route('/')
def home():
    global CTF_SITE_NAME
    return web_app_firewall.proxy('/', CTF_SITE_NAME, request, session())

@ctf_waf.route('/<path:path>',methods=['GET','POST'])
def proxy(path):
    global CTF_SITE_NAME
    return web_app_firewall.proxy(path, CTF_SITE_NAME, request, session())

if __name__ == '__main__':
    ctf_waf.run(host='0.0.0.0', debug = False, port=5001)