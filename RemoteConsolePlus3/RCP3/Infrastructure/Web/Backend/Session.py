#Created by Dmytro Konobrytskyi, 2014 (github.com/Akson)
from RCP3.Infrastructure.Web.Backend.StreamsTree import StreamsTree

class Session(object):
    def __init__(self):
        self._clientConnections = []
        self._streamsTree = StreamsTree()
    
    def RegisterClientConnection(self, clientConnection):
        self._clientConnections.append(clientConnection)
        
    def UnRegisterClientConnection(self, clientConnection):
        self._clientConnections.remove(clientConnection)
        
    def ProcessZmqMessage(self, zmqMessage, rawStreamName):
        (isNewNode, isSelectedNode) = self._streamsTree.FindStreamNode(rawStreamName)
        if isSelectedNode: 
            for clientConnection in self._clientConnections:
                clientConnection.write_message(zmqMessage)
                if isNewNode:
                    clientConnection.write_message("#ADDED_NEW_STREAM_NODE")
            
    def GetStreamsTree(self):
        return self._streamsTree