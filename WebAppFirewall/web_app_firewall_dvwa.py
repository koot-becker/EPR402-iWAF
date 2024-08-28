from flask import Flask,request,Response
import requests
import web_app_firewall
dvwa_waf = Flask(__name__)
DVWA_SITE_NAME = 'http://127.0.0.1:8002/'

@dvwa_waf.before_request
def before_request():
    return web_app_firewall.before_request(request, requests.session())

@dvwa_waf.route('/')
def home():
    global DVWA_SITE_NAME
    return web_app_firewall.proxy('/', DVWA_SITE_NAME, request, requests.session())

@dvwa_waf.route('/<path:path>',methods=['GET','POST'])
def proxy(path):
    global DVWA_SITE_NAME
    return web_app_firewall.proxy(path, DVWA_SITE_NAME, request, requests.session())

if __name__ == '__main__':
    dvwa_waf.run(host='0.0.0.0', debug = False, port=5002)