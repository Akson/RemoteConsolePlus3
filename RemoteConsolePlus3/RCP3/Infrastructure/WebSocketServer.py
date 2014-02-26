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
from RCP3.Infrastructure.StreamsCollector import StreamsCollector
from RCP3.Infrastructure.ZmqMessageProcessor import ZmqMessageProcessor
ioloop.install()

WebServerStopRequested = False

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        WebSocketPathDict = {}
        WebSocketPathDict["serverAddress"]=Config["Web server"]["Address"]
        WebSocketPathDict["serverPort"]=Config["Web server"]["Port"]
        WebSocketPathDict["sessionName"]=self.get_argument("sessionName")
        
        WebSocketPath = "ws://{serverAddress}:{serverPort}/WebSockets/?sessionName={sessionName}".format(**WebSocketPathDict)
        self.render("TestWebSockets.html", WebSocketPath=WebSocketPath)
                
class StreamsTreeRequestHandler(tornado.web.RequestHandler):
    _currentTree = {'text':'root', 'children':[], 'id':'root'}

    def CreateNewRandomTreeNode(self):
        rnadStr = 'node'+str(randint(0, 10000))
        return {'text':rnadStr, 'children':[], 'id':rnadStr}

    def GrowTree(self, newNodesNumber = 1):
        for i in range(newNodesNumber):
            curNode = StreamsTreeRequestHandler._currentTree
            while len(curNode['children']) > 0:
                if random.random()<(1.0/len(curNode['children'])):
                    break
                curNode = curNode['children'][randint(0, len(curNode['children'])-1)]
            curNode['children'].append(self.CreateNewRandomTreeNode())
    
    @tornado.web.asynchronous
    def get(self, params):
        print "tree requested", params
        if params == "":
            self.render("StreamsTreeViewer.html")
        else:
            #streamsTree = StreamsTreeRequestHandler._streamCollector.GetStreamsTree()
            #print json.dumps(streamsTree)
            self.GrowTree(10)
            self.set_header("Content-Type", 'application/json')
            self.write(json.dumps(StreamsTreeRequestHandler._currentTree))
            print json.dumps(StreamsTreeRequestHandler._currentTree)
            #self.write('<ul><li>Node 1</li><li class="jstree-closed">Node 2</li></ul>')
            self.flush()
            self.finish()
                
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def initialize(self, zmqMessageProcessor):
        self._zmqMessageProcessor = zmqMessageProcessor
        
    def open(self, *args):
        self._sessionName = self.get_argument("sessionName")
        print "open", self._sessionName
        self._zmqMessageProcessor.RegisterStreamListener(self._sessionName, self)
        self.stream.set_nodelay(True)

    def on_close(self):
        print "close"
        self._zmqMessageProcessor.UnRegisterStreamListener(self._sessionName, self)

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
        
        app = tornado.web.Application([
            (r'/Static/(.*)', tornado.web.StaticFileHandler, {'path': "./RCP3/Infrastructure/Static"}),
            (r'/Tmp/(.*)', tornado.web.StaticFileHandler, {'path': Config["Web server"]["Temporary files folder"]}),
            (r'/OutputConsole/', IndexHandler),
            (r'/StreamsTree/(.*)', StreamsTreeRequestHandler),
            (r'/WebSockets/', WebSocketHandler, dict(zmqMessageProcessor=zmqMessageProcessor)),
            
        ], debug=True)
        
        periodic = ioloop.PeriodicCallback(CheckServerStopRequests, 500)
        periodic.start()
        
        app.listen(Config["Web server"]["Port"])
        tornado.ioloop.IOLoop.instance().start() 
    except:
        print traceback.format_exc()
    
if __name__ == '__main__':
    Run(multiprocessing.queues.Queue())