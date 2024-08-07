from flask import Flask,request,Response
import requests
import web_app_firewall
dvwa_waf = Flask(__name__)
DVWA_SITE_NAME = 'http://127.0.0.1:8002/'

@dvwa_waf.before_request
def before_request():
    web_app_firewall.before_request()

@dvwa_waf.route('/')
def home():
    global DVWA_SITE_NAME
    web_app_firewall.proxy('/', DVWA_SITE_NAME, request)

@dvwa_waf.route('/<path:path>',methods=['GET','POST'])
def proxy(path):
    global DVWA_SITE_NAME
    web_app_firewall.proxy('/<path:path>', DVWA_SITE_NAME, request)

if __name__ == '__main__':
    dvwa_waf.run(host='0.0.0.0', debug = False, port=5002)