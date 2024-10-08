# Existing imports
from flask import Flask, render_template
import json
import logging

# Custom imports
# from web_app_firewall_interface import WebAppFirewallInterface

waf = Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True

@waf.route('/')
def home():
    with open('web_apps.json') as f:
        web_apps = json.load(f)
    return render_template('overview.html', wafs=web_apps)