# Web Application Firewall
## A reverse proxy that contains processing of requests and responses.

## web_app_firewall.py
This is the main module that should require no libraries to function except for communication.

## web_app_firewall_tiredful.py
This is the WAF interface for the Tiredful site. It spins up a transparent reverse proxy on port 5000 to access the Tiredful site and API.

## web_app_firewall_ctf.py
This is the WAF interface for the CTF-JWT site. It spins up a transparent reverse proxy on port 5001 to access the CTF-JWT site.

## web_app_firewall_dvwa.py
This is the WAF interface for the DVWA site. It spins up a transparent reverse proxy on port 5002 to access the DVWA site.

## web_app_firewall_interface.py
This is a module which interacts with and starts up each of the respective firewalls.