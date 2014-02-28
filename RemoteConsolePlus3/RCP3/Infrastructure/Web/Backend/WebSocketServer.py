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
import os
from RCP3.Infrastructure.Web.Backend.SessionsManager import SessionsManager
ioloop.install()

from random import randint, random

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
    def initialize(self, sessionsManager):
        self._zmqMessageProcessor = sessionsManager
        self._sessionManager = sessionsManager
        
    def open(self, *args):
        self._sessionId = self.get_argument("sessionId")
        print "WebSocket opened for session:", self._sessionId
        self._sessionManager.RegisterClientConnection(self._sessionId, self)
        self.stream.set_nodelay(True)

    def on_close(self):
        print "WebSocket closed for session:", self._sessionId
        self._sessionManager.UnRegisterClientConnection(self._sessionId, self)


class StreamsTreeRequestHandler(tornado.web.RequestHandler):
    _currentTree = {'text':'root', 'children':[], 'id':'root', 'state':{'selected':True}}

    def initialize(self, sessionsManager):
        self._sessionsManager = sessionsManager
        
    def CreateNewRandomTreeNode(self):
        rnadStr = 'node'+str(randint(0, 10000))
        return {'text':rnadStr, 'children':[], 'id':rnadStr}

    def GrowTree(self, newNodesNumber = 1):
        for i in range(newNodesNumber):
            curNode = StreamsTreeRequestHandler._currentTree
            while len(curNode['children']) > 0:
                if random()<(1.0/len(curNode['children'])):
                    break
                curNode = curNode['children'][randint(0, len(curNode['children'])-1)]
            curNode['children'].append(self.CreateNewRandomTreeNode())
    
    @tornado.web.asynchronous
    def get(self, params):
        print "tree requested", params, self.get_argument("sessionId")
        print self._sessionsManager.GetSessionTree(self.get_argument("sessionId")).GetTreeInJstreeFormat()
        #self.GrowTree(10)
        self.set_header("Content-Type", 'application/json')
        #self.write(json.dumps(StreamsTreeRequestHandler._currentTree))
        #print json.dumps(StreamsTreeRequestHandler._currentTree)
        
        self.write(json.dumps(self._sessionsManager.GetSessionTree(self.get_argument("sessionId")).GetTreeInJstreeFormat()))
        
        self.flush()
        self.finish()
        
        
WebServerStopRequested = False
def CheckServerStopRequests():
    if WebServerStopRequested:
        tornado.ioloop.IOLoop.instance().stop()

        
def Run():
    try:
        print "Running web server on port: "+str(Config["Web server"]["Port"])
        sessionsManager = SessionsManager()
        
        socket = zmq.Context.instance().socket(zmq.SUB)
        socket.bind("tcp://*:"+str(Config["Web server"]["IncomingZmqPort"]))
        socket.setsockopt(zmq.SUBSCRIBE, "")
        stream = ZMQStream(socket)
        stream.on_recv(sessionsManager.ProcessZmqMessages)
        
        settings = {
            "debug" : True,
            "template_path":os.path.join(os.path.dirname(__file__), "../Frontend"),
        }

        app = tornado.web.Application([
            (r'/Static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "../Frontend/Static")}),
            (r'/Tmp/(.*)', tornado.web.StaticFileHandler, {'path': Config["Web server"]["Temporary files folder"]}),
            (r'/OutputConsole/', IndexHandler),
            (r'/StreamsTree/(.*)', StreamsTreeRequestHandler, dict(sessionsManager=sessionsManager)),
            (r'/WebSockets/', WebSocketHandler, dict(sessionsManager=sessionsManager)),
            
        ], **settings)
        
        periodic = ioloop.PeriodicCallback(CheckServerStopRequests, 500)
        periodic.start()
        
        app.listen(Config["Web server"]["Port"])
        tornado.ioloop.IOLoop.instance().start() 
    except:
        print traceback.format_exc()
    
if __name__ == '__main__':
    Run(multiprocessing.queues.Queue())