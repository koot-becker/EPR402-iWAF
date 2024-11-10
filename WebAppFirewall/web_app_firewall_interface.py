# Existing imports
from flask import Flask, request
from requests import session, get, put
from optparse import OptionParser
import json
from datetime import datetime

# Custom imports
import web_app_firewall

# Public variables
__version__ = "0.1"

class WebAppFirewallInterface:
    def __init__(self, site_name='localhost', id=1):
        # Initialize the Flask app
        self.waf = Flask(__name__)
        self.id = id
        self.SITE_NAME = f'http://{site_name}:800{self.id}/'
        self.port = f'500{self.id}'

        # Get the settings and rules from the Database
        try:
            db = get(f'http://localhost:8000/api/wafs/{self.id}/').json()
        except:
            data = '{"settings": {"rule_settings": { "block_remote_addr": false, "block_user_agent": false, "block_path": false, "block_query_string": false }, "token_settings": { "check_token": true }, "signature_settings": { "check_signature": true }, "anomaly_settings": { "check_anomaly": false } }, "rules": { "blocked_ips": [], "blocked_user_agents": [], "blocked_paths": [], "blocked_query_strings": [] }, "total_requests": 0, "allowed_requests": 0, "blocked_requests": 0 , "waf_container_name": "CTF_WAF"}'
            db = json.loads(data)
        self.settings = db['settings']
        self.rules = db['rules']
        self.container_name = db['waf_container_name']
        self.total_requests = db['total_requests']
        self.allowed_requests = db['allowed_requests']
        self.blocked_requests = db['blocked_requests']
        self.total_time = db['total_time']

        self.waf.before_request(self.before_request)
        self.waf.after_request(self.after_request)
        self.waf.route('/', methods=['GET', 'POST'])(self.home)
        self.waf.route('/<path:path>', methods=['GET', 'POST'])(self.proxy)

        self.rtt = 1
        self.time_start = ""
        self.time = 0

    def before_request(self):
        self.time_start = datetime.now()
        response = web_app_firewall.before_request(request, session(), self.settings, self.rules, self.container_name)
        self.total_requests += 1
        if response:
            self.blocked_requests += 1
            return response
        else:
            self.allowed_requests += 1
        return

    def after_request(self, response, db={}):
        web_app_firewall.post_request(request, self.time, self.rtt)
        self.total_time += (self.time / self.rtt) * 100
        try:
            db['total_requests'] = self.total_requests
            db['allowed_requests'] = self.allowed_requests
            db['blocked_requests'] = self.blocked_requests
            db['total_time'] = self.total_time
            put(f'http://localhost:8000/api/wafs/{self.id}/', json=db)
        except:
            pass
        return response

    def home(self):
        self.time = (datetime.now()-self.time_start).total_seconds()
        response = web_app_firewall.proxy('/', self.SITE_NAME, request, session())
        self.rtt = response[1]
        return response[0]

    def proxy(self, path):
        self.time = (datetime.now()-self.time_start).total_seconds()
        response = web_app_firewall.proxy(path, self.SITE_NAME, request, session())
        self.rtt = response[1]
        return response[0]

    def run(self):
        self.waf.run(host='0.0.0.0', port=self.port)

def parse_options():
    usage = r'usage: python3 %prog [options] -i ID -u URL'
    parser = OptionParser(usage = usage, version = __version__)

    parser.add_option('-i', '--id',
        action = 'store',
        type = 'string',
        dest = 'id',
        help = 'The WAF ID.'
    )

    parser.add_option('-u', '--url',
        action = 'store',
        type = 'string',
        dest = 'url',
        help = 'The App URL.'
    )

    options, args = parser.parse_args()
    if options.id == None:
        parser.print_help()
        parser.error("Missing options.")
        
    return options

if __name__ == '__main__':
    options = parse_options()
    if options.url == None:
        waf_interface = WebAppFirewallInterface(id=options.id)
    else:
        waf_interface = WebAppFirewallInterface(site_name=options.url, id=options.id)
    waf_interface.run()