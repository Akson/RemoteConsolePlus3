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

class Proxy(object):
    _clientsConnectedToStreams = {}
    _clientsListLock = threading.Lock()
    
    @staticmethod
    def RegisterStreamListener(streamName, streamListener):
        with Proxy._clientsListLock: 
            if not streamName in Proxy._clientsConnectedToStreams:
                Proxy._clientsConnectedToStreams[streamName] = []
            Proxy._clientsConnectedToStreams[streamName].append(streamListener)
        
    @staticmethod
    def UnRegisterStreamListener(streamName, streamListener):
        with Proxy._clientsListLock: 
            Proxy._clientsConnectedToStreams[streamName].remove(streamListener)
        
    @staticmethod
    def SendMessageToClients(streamName, message):
        if streamName not in Proxy._clientsConnectedToStreams:
            return
        with Proxy._clientsListLock: 
            for client in Proxy._clientsConnectedToStreams[streamName]:
                try:
                    client.write_message(json.dumps(message))
                except:
                    pass #THIS IS A DIRTY HACK!!! TORNADO IS NOT THREAD SAFE!!!

    @staticmethod
    def ProxyThreadFunction(inputQueue):
        while True:
            try:
                incomingObject = inputQueue.get(True, 1)
                incomingDict = json.loads(incomingObject)
                Proxy.SendMessageToClients(incomingDict["StreamName"], incomingDict["Message"])
            except Empty:
                pass

class IndexHandler(tornado.web.RequestHandler):
    _streamCollector = None
    @tornado.web.asynchronous
    def get(self):
        WebSocketPathDict = {}
        WebSocketPathDict["serverAddress"]=Config["Web server"]["Address"]
        WebSocketPathDict["serverPort"]=Config["Web server"]["Port"]
        WebSocketPathDict["streamName"]=self.get_argument("streamName")
        
        WebSocketPath = "ws://{serverAddress}:{serverPort}/WebSockets/?streamName={streamName}".format(**WebSocketPathDict)
        self.render("TestWebSockets.html", WebSocketPath=WebSocketPath)
                
class StreamsTreeRequestHandler(tornado.web.RequestHandler):
    _streamCollector = None
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
        print "open"
        self._streamName = self.get_argument("streamName")
        Proxy.RegisterStreamListener(self._streamName, self)
        self.stream.set_nodelay(True)

    def on_close(self):
        print "close"
        Proxy.UnRegisterStreamListener(self._streamName, self)

def Run(proxyInputqueue, streamCollector):
    try:
        print "Running websocket server on port: "+str(Config["Web server"]["Port"])
        StreamsTreeRequestHandler._streamCollector = streamCollector
        
        thread = Thread(target = Proxy.ProxyThreadFunction, args = (proxyInputqueue, ))
        thread.start()
        
        app = tornado.web.Application([
            (r'/Static/(.*)', tornado.web.StaticFileHandler, {'path': "./RCP3/Infrastructure/Static"}),
            (r'/Tmp/(.*)', tornado.web.StaticFileHandler, {'path': Config["Web server"]["Temporary files folder"]}),
            (r'/OutputConsole/', IndexHandler),
            (r'/StreamsTree/(.*)', StreamsTreeRequestHandler),
            (r'/WebSockets/', WebSocketHandler),
            
        ], debug=True)
        
        app.listen(Config["Web server"]["Port"])
        tornado.ioloop.IOLoop.instance().start()
        thread.join()
    except:
        print traceback.format_exc()
    
proxyQueue = None
    
if __name__ == '__main__':
    RunWebSocketsServer(multiprocessing.queues.Queue())