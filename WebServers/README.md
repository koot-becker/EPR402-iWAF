# Web Applications on Docker

## Web Application 1 - Tiredful API
### Access through port 8000
```
cd /home/administrator/EPR402/WebServers/Tiredful;
source .tiredful_venv/bin/activate;
docker build -t tiredful .;
docker run -p 8000:8000 --name tiredful -it tiredful;
```
## Web Application 1 - JWT CTF
### Access through port 8001
```
cd /home/administrator/EPR402/WebServers/ctf-jwt-token;
source .jwt_venv/bin/activate;
cd target-website;
docker build -t ctf-jwt-token .;
docker run --rm -p 8001:8080 --name ctf-jwt-token -it ctf-jwt-token;
```

## Web Application 2 - DVWA
### Access through port 8002
```
cd /home/administrator/EPR402/WebServers/DVWA;
source .dvwa_venv/bin/activate;
docker build -t dvwa .;
docker run --rm -it -p 8002:80 --name dvwa -it dvwa;
```