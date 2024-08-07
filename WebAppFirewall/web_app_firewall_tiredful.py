from flask import Flask,request,Response
import requests
import web_app_firewall
tiredful_waf = Flask(__name__)
TIREDFUL_SITE_NAME = 'http://127.0.0.1:8000/'

@tiredful_waf.before_request
def before_request():
    web_app_firewall.before_request()

@tiredful_waf.route('/')
def home():
    global TIREDFUL_SITE_NAME
    web_app_firewall.proxy('/', TIREDFUL_SITE_NAME, request)

@tiredful_waf.route('/<path:path>',methods=['GET','POST'])
def proxy(path):
    global TIREDFUL_SITE_NAME
    web_app_firewall.proxy('/<path:path>', TIREDFUL_SITE_NAME, request)

if __name__ == '__main__':
    tiredful_waf.run(host='0.0.0.0', debug = False, port=5001)