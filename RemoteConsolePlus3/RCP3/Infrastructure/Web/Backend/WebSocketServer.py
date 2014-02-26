#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import tornado.ioloop
import tornado.websocket
from threading import Thread
import threading
import json
from Queue import Empty
import multiprocessing.queues
import tornado.template
from RCP3.Configuration import Config
from random import randint
import random
import traceback

import zmq

from zmq.eventloop import ioloop
from zmq.eventloop.zmqstream import ZMQStream
from RCP3.Infrastructure.Web.Backend.ZmqMessageProcessor import ZmqMessageProcessor
from RCP3.Infrastructure.Web.Backend.StreamsTreeManager import StreamsTreeRequestHandler
import os
ioloop.install()

WebServerStopRequested = False

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        pathDict = {}
        pathDict["serverAddress"]=Config["Web server"]["Address"]
        pathDict["serverPort"]=Config["Web server"]["Port"]
        pathDict["sessionId"]=self.get_argument("sessionId")
        
        webSocketPath = "ws://{serverAddress}:{serverPort}/WebSockets/?sessionId={sessionId}".format(**pathDict)
        self.render("RCP.html", WebSocketPath=webSocketPath, SessionId=self.get_argument("sessionId"))
                
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, zmqMessageProcessor):
        self._zmqMessageProcessor = zmqMessageProcessor
        
    def open(self, *args):
        self._sessionId = self.get_argument("sessionId")
        print "open", self._sessionId
        self._zmqMessageProcessor.RegisterStreamListener(self._sessionId, self)
        self.stream.set_nodelay(True)

    def on_close(self):
        print "close"
        self._zmqMessageProcessor.UnRegisterStreamListener(self._sessionId, self)

def CheckServerStopRequests():
    if WebServerStopRequested:
        tornado.ioloop.IOLoop.instance().stop()
        
def Run():
    try:
        print "Running web server on port: "+str(Config["Web server"]["Port"])
        
        zmqMessageProcessor = ZmqMessageProcessor()
        
        socket = zmq.Context.instance().socket(zmq.SUB)
        socket.bind("tcp://*:"+str(Config["Web server"]["IncomingZmqPort"]))
        socket.setsockopt(zmq.SUBSCRIBE, "")
        stream = ZMQStream(socket)
        stream.on_recv(zmqMessageProcessor.OnIncomingZmqMessage)
        
        
        settings = {
            "debug" : True,
            "template_path":os.path.join(os.path.dirname(__file__), "../Frontend"),
        }

        app = tornado.web.Application([
            (r'/Static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "../Frontend/Static")}),
            (r'/Tmp/(.*)', tornado.web.StaticFileHandler, {'path': Config["Web server"]["Temporary files folder"]}),
            (r'/OutputConsole/', IndexHandler),
            (r'/StreamsTree/(.*)', StreamsTreeRequestHandler, dict(zmqMessageProcessor=zmqMessageProcessor)),
            (r'/WebSockets/', WebSocketHandler, dict(zmqMessageProcessor=zmqMessageProcessor)),
            
        ], **settings)
        
        periodic = ioloop.PeriodicCallback(CheckServerStopRequests, 500)
        periodic.start()
        
        app.listen(Config["Web server"]["Port"])
        tornado.ioloop.IOLoop.instance().start() 
    except:
        print traceback.format_exc()
    
if __name__ == '__main__':
    Run(multiprocessing.queues.Queue())