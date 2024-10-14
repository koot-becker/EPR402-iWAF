# Existing imports
from flask import Flask, request
from requests import session, get
from optparse import OptionParser

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
        db = get(f'http://localhost:8000/api/wafs/{self.id}/').json()
        self.settings = db['settings']
        self.rules = db['rules']

        self.waf.before_request(self.before_request)
        self.waf.after_request(self.after_request)
        self.waf.route('/')(self.home)
        self.waf.route('/<path:path>', methods=['GET', 'POST'])(self.proxy)

    def before_request(self):
        web_app_firewall.before_request(request, session(), self.settings, self.rules)

    def after_request(self, response):
        web_app_firewall.post_request(request)
        return response

    def home(self):
        return web_app_firewall.proxy('/', self.SITE_NAME, request, session())

    def proxy(self, path):
        return web_app_firewall.proxy(path, self.SITE_NAME, request, session())

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