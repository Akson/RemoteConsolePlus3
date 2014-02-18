'''Created by Dmytro Konobrytskyi, 2013(C)'''

import zmq
import time

import collections
import json

def Tree():
    return collections.defaultdict(Tree)

class StreamsCollector(object):
    def __init__(self, routerAddress):
        '''
        Here we initialize input and output ZMQ sockets
        '''
        self._routerAddress = routerAddress
        
        #Initialize ZMQ
        self._context = zmq.Context.instance()
        
        #Create an input socket and subscribe for everything
        self._inputSocket = self._context.socket(zmq.SUB)
        self._inputSocket.connect(self._routerAddress)
        self._inputSocket.setsockopt(zmq.SUBSCRIBE, "")
        
        self._root = Tree()

    def Run(self):
        while True:
            try:
                message = self._inputSocket.recv()
                streamName = message[:message.find(chr(0))]
                self.ProcessStreamname(streamName)
            except zmq.ZMQError, e:
                print e
                time.sleep(0.001)

    def ProcessStreamname(self, rawStreamName):
        #print rawStreamName
        #print json.dumps(self._root)
        streamName = rawStreamName[:-1]
        streamComponents = streamName.split("/")
        curNode = self._root
        for component in streamComponents:
            if component not in curNode:
                curNode[component] = Tree()
            curNode = curNode[component]
            
    def GetStreamsTree(self):
        return self._root
