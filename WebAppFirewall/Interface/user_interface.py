# Existing imports
from flask import Flask, request, render_template
from requests import session

# Custom imports

class WebAppFirewallInterface:
    def __init__(self, host='0.0.0.0', port=5123, debug=False):
        self.waf = Flask(__name__)
        self.host = host
        self.port = port
        self.debug = debug

        self.waf.route('/')(self.home)

    def home(self):
        waf_1 = {'name': 'Web Application 1', 'total_requests': 100, 'allowed_requests': 50, 'blocked_requests': 50, 'threats_detected': 5, 'signature_graph_url': 'static/signature_graph.png', 'outlier_graph_url': 'static/svm_graph.png'}
        waf_2 = {'name': 'Web Application 2', 'total_requests': 100, 'allowed_requests': 50, 'blocked_requests': 50, 'threats_detected': 5, 'signature_graph_url': 'static/signature_graph.png', 'outlier_graph_url': 'static/svm_graph.png'}
        waf_3 = {'name': 'Web Application 3', 'total_requests': 100, 'allowed_requests': 50, 'blocked_requests': 50, 'threats_detected': 5, 'signature_graph_url': 'static/signature_graph.png', 'outlier_graph_url': 'static/svm_graph.png'}
        return render_template('overview.html', wafs=[waf_1, waf_2, waf_3])

    def run(self):
        self.waf.run(host=self.host, port=self.port, debug=self.debug)

if __name__ == '__main__':
    waf_interface = WebAppFirewallInterface()
    waf_interface.run()