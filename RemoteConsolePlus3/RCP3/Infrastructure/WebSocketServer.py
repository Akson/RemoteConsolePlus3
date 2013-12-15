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
    @tornado.web.asynchronous
    def get(self):
        WebSocketPathDict = {}
        WebSocketPathDict["serverAddress"]=Config["Web server"]["Address"]
        WebSocketPathDict["serverPort"]=Config["Web server"]["Port"]
        WebSocketPathDict["streamName"]=self.get_argument("streamName")
        
        WebSocketPath = "ws://{serverAddress}:{serverPort}/WebSockets/?streamName={streamName}".format(**WebSocketPathDict)
        self.render("TestWebSockets.html", WebSocketPath=WebSocketPath)
                
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self, *args):
        print "open"
        self._streamName = self.get_argument("streamName")
        Proxy.RegisterStreamListener(self._streamName, self)
        self.stream.set_nodelay(True)

    def on_close(self):
        print "close"
        Proxy.UnRegisterStreamListener(self._streamName, self)

def RunWebSocketsServer(proxyInputqueue):
    print "RunWebSocketsServer..."
    thread = Thread(target = Proxy.ProxyThreadFunction, args = (proxyInputqueue, ))
    thread.start()
    
    app = tornado.web.Application([
        (r'/Tmp/(.*)', tornado.web.StaticFileHandler, {'path': Config["Web server"]["Temporary files folder"]}),
        (r'/OutputConsole/', IndexHandler),
        (r'/WebSockets/', WebSocketHandler),
    ], debug=False)
    
    app.listen(Config["Web server"]["Port"])
    tornado.ioloop.IOLoop.instance().start()
    thread.join()
    
proxyQueue = None
    
if __name__ == '__main__':
    RunWebSocketsServer(multiprocessing.queues.Queue())