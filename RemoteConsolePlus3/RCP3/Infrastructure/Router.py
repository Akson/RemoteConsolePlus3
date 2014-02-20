'''Created by Dmytro Konobrytskyi, 2012(C)'''

import zmq
import traceback

class Router(object):
    def __init__(self, inputAddress, outputAddress):
        '''
        Here we initialize input and output ZMQ sockets
        '''
        self._inputAddress = inputAddress
        self._outputAddress = outputAddress
        
        #Initialize ZMQ
        self._context = zmq.Context()
        
        #Create an input socket and subscribe for everything
        self._inputSocket = self._context.socket(zmq.XSUB)
        self._inputSocket.bind(self._inputAddress)

        #Create an output socket
        self._outputSocket = self._context.socket(zmq.XPUB)
        self._outputSocket.bind(self._outputAddress)

    def Run(self):
        try:
            print "Running router: "+self._inputAddress+" -> "+self._outputAddress
            zmq.proxy(self._inputSocket, self._outputSocket, None)
        except:
            print traceback.format_exc()
            print "Probably another router is already running."
