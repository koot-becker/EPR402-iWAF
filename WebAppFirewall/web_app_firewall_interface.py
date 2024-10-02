# Existing imports
from flask import Flask, request
from requests import session

# Custom imports
import web_app_firewall

class WebAppFirewallInterface:
    def __init__(self, site_name, host='0.0.0.0', port=5000, debug=False):
        self.waf = Flask(__name__)
        self.CTF_SITE_NAME = site_name
        self.host = host
        self.port = port
        self.debug = debug

        self.waf.before_request(self.before_request)
        self.waf.after_request(self.after_request)
        self.waf.route('/')(self.home)
        self.waf.route('/<path:path>', methods=['GET', 'POST'])(self.proxy)

    def before_request(self):
        web_app_firewall.before_request(request, session())

    def after_request(self, response):
        web_app_firewall.post_request(request)
        return response

    def home(self):
        return web_app_firewall.proxy('/', self.CTF_SITE_NAME, request, session())

    def proxy(self, path):
        return web_app_firewall.proxy(path, self.CTF_SITE_NAME, request, session())

    def run(self):
        self.waf.run(host=self.host, port=self.port, debug=self.debug)

if __name__ == '__main__':
    waf_interface = WebAppFirewallInterface(site_name='http://127.0.0.1:8001/')
    waf_interface.run()