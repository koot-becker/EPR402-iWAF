# Web Application Firewall
A reverse proxy that contains processing of requests and responses. It contains rule-based detection, attack signature detection, and behavioural anomaly detection.

## web_app_firewall_interface.py
This is a module which interacts with and starts up each of the respective firewall.
```
python3.12 web_app_firewall_interface.py --id <id> --url <app_destination_ip>
```

## Docker
```
docker build -t waf .;
docker run --network host --name <app_name>_WAF waf;
```