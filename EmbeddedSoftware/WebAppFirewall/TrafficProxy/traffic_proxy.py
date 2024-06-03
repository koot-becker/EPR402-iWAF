#!/usr/bin/env python
import tornado.ioloop
import maproxy.proxyserver

server = maproxy.proxyserver.ProxyServer("localhost/DVWA/login.php",8080)
server.listen(81)
print("http://127.0.0.1:81 -> http://localhost/DVWA/login.php")
tornado.ioloop.IOLoop.instance().start()