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
        self.waf.route('/web_app_1/', methods=['GET', 'POST'])(self.web_app_1)
        self.waf.route('/web_app_2/', methods=['GET', 'POST'])(self.web_app_2)
        self.waf.route('/web_app_3/', methods=['GET', 'POST'])(self.web_app_3)

    def home(self):
        # return render_template('main.html', web_applications=[{'name': 'Web Application 1', 'path': '/web_app_1'}, {'name': 'Web Application 2', 'path': '/web_app_2'}, {'name': 'Web Application 3', 'path': '/web_app_3'}])
        return render_template('overview.html')


    def web_app_1(self):
        return render_template('web_app_1.html', web_application={'name': 'Web Application 1'})
    
    def web_app_2(self):
        return render_template('web_app_2.html', web_application={'name': 'Web Application 2'})
    
    def web_app_3(self):
        return render_template('web_app_3.html', web_application={'name': 'Web Application 3'})

    def run(self):
        self.waf.run(host=self.host, port=self.port, debug=self.debug)

if __name__ == '__main__':
    waf_interface = WebAppFirewallInterface()
    waf_interface.run()