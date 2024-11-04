# Web Applications on Docker

## Web Application 1 - Tiredful API
### Access through port 8000
```
cd /home/administrator/EPR402/WebServers/Tiredful;
source .tiredful_venv/bin/activate;
docker build -t tiredful .;
docker run -dp 8001:8000 --name tiredful -it tiredful;
```
## Web Application 2 - JWT CTF
### Access through port 8001
```
cd /home/administrator/EPR402/WebServers/ctf-jwt-token;
source .jwt_venv/bin/activate;
cd target-website;
docker build -t ctf-jwt-token .;
docker run -dp 8002:8080 --name ctf-jwt-token -it ctf-jwt-token;
```

## Web Application 3 - DVWA
### Access through port 8002
```
cd /home/administrator/EPR402/WebServers/DVWA;
docker compose up -d
```