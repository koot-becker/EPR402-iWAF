# Intelligent Web App Firewall using JWT Inspection

![Functional Block Diagram](https://github.com/KootBecker/EPR402/assets/153346628/11eac9e5-f336-4210-9d2f-0b59efe1341f)

## User Interface
- The User Interface directory contains the WAF web management interface written in ReactJS with a REST API - Django backend.

## Traffic Simulator
- The Traffic Simulator contains the Action Generator, Exploit Injector and User Simulator for testing purposes.
- Run before WebAppFirewall.

## WebAppFirewall
- The WAF contains the Traffic Interceptor, JWT Extractor, Basic Allow/Deny Logic Unit, Baseline Trainer, Anomaly Logger, Traffic Analyser and Traffic Proxy
- Run natively with Python3.12 or use the dockerised version.
- Run natively after UI or dockerised from UI.

##  Web Servers
- The Web Servers are contained within this directory. Run as dockers.
