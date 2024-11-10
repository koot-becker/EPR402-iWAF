# Web Application Firewall
## A reverse proxy that contains processing of requests and responses.

## web_app_firewall.py
This is the main module that should require no libraries to function except for communication.

## web_app_firewall_interface.py
docker run -d --network host --name CTF_WAF waf --id 2 --url "192.168.8.9"
python3.12 web_app_firewall_interface.py --id 2 --url "192.168.8.9"