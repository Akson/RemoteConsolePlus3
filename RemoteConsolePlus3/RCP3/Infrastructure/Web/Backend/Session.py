#Created by Dmytro Konobrytskyi, 2014 (github.com/Akson)

class Session(object):
    def __init__(self):
        self._clientConnections = []
        self._streamsTreeRoot = {}
    
    def RegisterClientConnection(self, clientConnection):
        self._clientConnections.append(clientConnection)
        
    def UnRegisterClientConnection(self, clientConnection):
        self._clientConnections.remove(clientConnection)
        
    def ProcessZmqMessage(self, zmqMessage, rawStreamName):
        if self.EnabledStream(rawStreamName): 
            for clientConnection in self._clientConnections:
                clientConnection.write_message(zmqMessage)
            
    def EnabledStream(self, rawStreamName):
        print self._streamsTreeRoot
        streamName = rawStreamName[:-1]
        streamComponents = streamName.split("/")
        curNode = self._streamsTreeRoot
        for component in streamComponents:
            if component not in curNode:
                curNode[component] = {}
            curNode = curNode[component]
        
        return True