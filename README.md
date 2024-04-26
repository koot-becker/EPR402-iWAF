# EPR402 - TG4: Web Application Firewall using JSON Web Tokens

![Functional Block Diagram](https://github.com/KootBecker/EPR402/assets/153346628/11eac9e5-f336-4210-9d2f-0b59efe1341f)

## The User Interface and Traffic Simulator are contained within the ClientSoftware directory
- The User Interface directory contains the WAF web management interface
- The Traffic Simulator contains the Action Generator, Exploit Injector and User Simulator

## The WAF and web servers are contained within the EmbeddedSoftware directory
- The WAF contains the Traffic Interceptor, JWT Extractor, Basic Allow/Deny Logic Unit, Baseline Trainer, Anomaly Logger, Traffic Analyser and Traffic Proxy
- The web servers contain web servers 1-3
