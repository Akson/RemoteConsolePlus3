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
ioloop.install()

WebServerStopRequested = False

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        WebSocketPathDict = {}
        WebSocketPathDict["serverAddress"]=Config["Web server"]["Address"]
        WebSocketPathDict["serverPort"]=Config["Web server"]["Port"]
        WebSocketPathDict["streamName"]=self.get_argument("streamName")
        
        WebSocketPath = "ws://{serverAddress}:{serverPort}/WebSockets/?streamName={streamName}".format(**WebSocketPathDict)
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
            streamsTree = StreamsTreeRequestHandler._streamCollector.GetStreamsTree()
            print json.dumps(streamsTree)
            self.GrowTree(10)
            self.set_header("Content-Type", 'application/json')
            self.write(json.dumps(StreamsTreeRequestHandler._currentTree))
            print json.dumps(StreamsTreeRequestHandler._currentTree)
            #self.write('<ul><li>Node 1</li><li class="jstree-closed">Node 2</li></ul>')
            self.flush()
            self.finish()
                
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        self._streamName = self.get_argument("streamName")
        print "open", self._streamName
        Proxy.RegisterStreamListener(self._streamName, self)
        self.stream.set_nodelay(True)

    def on_close(self):
        print "close"
        Proxy.UnRegisterStreamListener(self._streamName, self)

class Proxy(object):
    _clientsConnectedToStreams = {}
    
    @staticmethod
    def RegisterStreamListener(streamName, streamListener):
        if not streamName in Proxy._clientsConnectedToStreams:
            Proxy._clientsConnectedToStreams[streamName] = []
        Proxy._clientsConnectedToStreams[streamName].append(streamListener)
        
    @staticmethod
    def UnRegisterStreamListener(streamName, streamListener):
        Proxy._clientsConnectedToStreams[streamName].remove(streamListener)

def OnIncomingZmqMessage(zmqMessages):
    for zmqMessage in zmqMessages:
        for client in Proxy._clientsConnectedToStreams["DefaultConsole"]:
            client.write_message(zmqMessage)

def CheckServerStopRequests():
    if WebServerStopRequested:
        tornado.ioloop.IOLoop.instance().stop() 
        
def Run():
    try:
        print "Running web server on port: "+str(Config["Web server"]["Port"])
        
        socket = zmq.Context.instance().socket(zmq.SUB)
        socket.bind("tcp://*:"+str(Config["Web server"]["IncomingZmqPort"]))
        socket.setsockopt(zmq.SUBSCRIBE, "")
        stream = ZMQStream(socket)
        stream.on_recv(OnIncomingZmqMessage)
        
        app = tornado.web.Application([
            (r'/Static/(.*)', tornado.web.StaticFileHandler, {'path': "./RCP3/Infrastructure/Static"}),
            (r'/Tmp/(.*)', tornado.web.StaticFileHandler, {'path': Config["Web server"]["Temporary files folder"]}),
            (r'/OutputConsole/', IndexHandler),
            (r'/StreamsTree/(.*)', StreamsTreeRequestHandler),
            (r'/WebSockets/', WebSocketHandler),
            
        ], debug=True)
        
        periodic = ioloop.PeriodicCallback(CheckServerStopRequests, 500)
        periodic.start()
        
        app.listen(Config["Web server"]["Port"])
        tornado.ioloop.IOLoop.instance().start() 
    except:
        print traceback.format_exc()
    
if __name__ == '__main__':
    Run(multiprocessing.queues.Queue())