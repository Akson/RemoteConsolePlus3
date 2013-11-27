#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import zmq
import thread
import unicodedata

class Backend(object):
    def __init__(self, parentNode):
        self._parentNode = parentNode
        
        self._streamsList = None
        self._serverAddress = None

        self._listeningThreadRunning = False
        self._stopListening = False
        self._reconnectToServer = False

        self.threadStopWaitTimeMs = 200
    
    def Delete(self):
        self._stopListening = True
    
    def GetParameters(self):
        return {"streamsList":self._streamsList, "serverAddress":self._serverAddress}
    
    def SetParameters(self, parameters):
        self._streamsList = parameters.get("streamsList", [])
        self._serverAddress = parameters.get("serverAddress", None)
        
        if self._serverAddress:
            self._reconnectToServer = True
            if not self._listeningThreadRunning:
                thread.start_new_thread(self.StreamListenerThreadFunc, ())
        
        
        
    def StreamListenerThreadFunc(self):
        while not self._stopListening:
            #Reconnect to server if needed
            if self._reconnectToServer:
                socket = zmq.Context.instance().socket(zmq.SUB)
                socket.connect(self._serverAddress)
                for streamName in self._streamsList:
                    socket.setsockopt(zmq.SUBSCRIBE, str(streamName))
                self._reconnectToServer = False

            #Wait for incoming messages 
            if socket.poll(self.threadStopWaitTimeMs) and not self._stopListening:
                try:
                    zmqMessage = socket.recv()
                except zmq.ZMQError, e:
                    print e
                self.ProcessIncomingZmqMessage(zmqMessage)

    def ProcessIncomingZmqMessage(self, zmqMessage):
        print zmqMessage
