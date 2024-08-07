from flask import Flask,request,Response
import requests
import web_app_firewall
ctf_waf = Flask(__name__)
CTF_SITE_NAME = 'http://127.0.0.1:8001/'

@ctf_waf.before_request
def before_request():
    web_app_firewall.before_request()

@ctf_waf.route('/')
def home():
    global CTF_SITE_NAME
    web_app_firewall.proxy('/', CTF_SITE_NAME, request)

@ctf_waf.route('/<path:path>',methods=['GET','POST'])
def proxy(path):
    global CTF_SITE_NAME
    web_app_firewall.proxy('/<path:path>', CTF_SITE_NAME, request)

if __name__ == '__main__':
    ctf_waf.run(host='0.0.0.0', debug = False, port=5001)