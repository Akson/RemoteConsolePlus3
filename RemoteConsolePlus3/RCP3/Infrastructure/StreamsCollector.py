'''Created by Dmytro Konobrytskyi, 2013(C)'''

import zmq
import time

class StreamsCollector(object):
    def __init__(self, routerAddress):
        '''
        Here we initialize input and output ZMQ sockets
        '''
        self._routerAddress = routerAddress
        
        #Initialize ZMQ
        self._context = zmq.Context()
        
        #Create an input socket and subscribe for everything
        self._inputSocket = self._context.socket(zmq.SUB)
        self._inputSocket.connect(self._routerAddress)
        self._inputSocket.setsockopt(zmq.SUBSCRIBE, "")
        
        self._streamsSet = set()

    def Run(self):
        while True:
            try:
                message = self._inputSocket.recv()
                streamName = message[:message.find(chr(0))]
                if streamName not in self._streamsSet:
                    self._streamsSet.add(streamName)
                    print self._streamsSet
            except zmq.ZMQError, e:
                print e
                time.sleep(0.001)
