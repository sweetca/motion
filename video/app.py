import os
import sys
import time

from session import Session
from daemon import Daemon

from flask import Flask, render_template, Response, jsonify
from flask_sockets import Sockets

def stopSession():
    if not Session.busy:
        return True
    Session.busy = False
    Session.timeStamp = int(time.time()*1000)
    Session().stopYoutube()

def startSession():
    if Session.busy:
        return True
    Session.busy = True
    Session.timeStamp = int(time.time()*1000)
    Session().runYoutube() 

def toJSON():
    return jsonify(respnse = "OK",
                   users = len(Session.subscribers),
                   session = Session.busy,
                   timestamp = Session.timeStamp,
                   youtubeStream = Session.streamYtb)

app = Flask(__name__)
sockets = Sockets(app)
server = None

def toR():
    return '{"session": ' + str(Session.busy).lower() + ', "timestamp": ' + str(Session.timeStamp) + '}'

def notify():
    for i in range(len(Session.subscribers)):
        print 'i', id(Session.subscribers[i])
        Session.subscribers[i].send(toR())
        
def unsubscribe(w):
    for i in range(len(Session.subscribers)):
        if id(Session.subscribers[i]) == id(w):
            Session.subscribers.pop(i)
            return

@sockets.route('/subscribe')
def echo_socket(ws):
    try:
        while True:
            message = ws.receive()
            ws.send(toR())
            Session.subscribers.append(ws)
    except:
        unsubscribe(ws)

@app.route('/')
def index():
    return render_template('index.html', channel = Session.channel)

@app.route('/api')
def api():
    return toJSON()

@app.route('/occupied')
def occupied():
    startSession()
    notify()
    return toJSON()

@app.route('/free')
def free():
    stopSession()
    notify()
    return toJSON()

class FlaskDaemon(Daemon):
    def run(self):
        server.serve_forever()
        
if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)

    daemon = FlaskDaemon(str(os.path.dirname(os.path.realpath(__file__))) + '/deamon.pid')
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        else:
            print "Unknown command"
            sys.exit(2)
        sys.exit(0)
    else:
        print "usage: %s start|stop|restart" % sys.argv[0]
        sys.exit(2)