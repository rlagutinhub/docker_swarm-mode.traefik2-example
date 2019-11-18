#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
 
import os
import sys
import json
import socket
import psutil
 
from flask import Flask, request
 
VISITS = 0
 
app = Flask(__name__)
 
 
def getsocket(pid):
 
    for c in psutil.net_connections(kind='inet'):
 
        if c.pid == int(pid) and c.status == 'ESTABLISHED':
 
            return "%s:%s" % (c.laddr)
 
 
@app.route("/")
def hello():
 
    global VISITS
 
    VISITS += 1
 
    html = "<html><head><title>HELLO</title></head>" \
        "<style>" \
        "body {" \
        "background-color: white;" \
        "text-align: left;" \
        "padding: 50px;" \
        "font-family: 'Open Sans','Helvetica Neue',Helvetica,Arial,sans-serif;" \
        "}" \
        "</style>" \
        "</head>" \
        "<body>"
 
    html += "<h2>Hello from <font color='#337ab7'>{name}</font></h2>".format(name=request.host)
    html += "<b>Backend hostname:</b> {hostname}<br>".format(hostname=socket.gethostname())
    html += "<b>Backend socket:</b> {socket}<br>".format(socket=getsocket(os.getpid()))
    html += "<br>"
 
    html += "<b>Visits:</b> {visits}<br>".format(visits=VISITS)
 
    if request.url:
 
        html += "<b>Request Url: </b>" + str(request.url) + "<br>"
        html += "<b>Request Path: </b>" + str(request.path) + "<br>"
        html += "<b>Request Method: </b>" + str(request.method) + "<br>"
        html += "<br><hr>"
 
    if request.headers:
 
        html += "<h4>Headers:</h4>"
 
        for headers_key, headers_value in request.headers.items():
 
            html += headers_key + ": " + headers_value + "<br>"
 
        html += "<br><hr>"
 
 
    return html
 
 
if __name__ == "__main__":
 
    if len(sys.argv) == 2:
        app.run(host='0.0.0.0', port=int(sys.argv[1]), debug=True)
 
    else:
        app.run(host='0.0.0.0', debug=True)
