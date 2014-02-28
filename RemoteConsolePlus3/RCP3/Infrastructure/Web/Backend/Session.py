#Created by Dmytro Konobrytskyi, 2014 (github.com/Akson)

class StreamsTreeNode(dict):
    def __init__(self):
        self._enabled = True
        
class StreamsTree(object):
    def __init__(self):
        self._root = StreamsTreeNode()
        
    def IsEnabledStream(self, rawStreamName):
        streamName = rawStreamName[:-1]
        streamComponents = streamName.split("/")
        curNode = self._root
        for component in streamComponents:
            if component not in curNode:
                curNode[component] = StreamsTreeNode()
            curNode = curNode[component]
        
        return True

    def GetTreeInJstreeFormat(self):
        return self.ConvertStreamsTreeNodeIntoJstreeNode(self._root, ['#'])

    def ConvertStreamsTreeNodeIntoJstreeNode(self, node, namesStack):
        jsNode = {}
        jsNode['id'] = "/".join(namesStack)
        jsNode['text'] = namesStack[-1]
        jsNode['state'] = {'selected':node._enabled}
        
        children = []
        for childName in node:
            children.append(self.ConvertStreamsTreeNodeIntoJstreeNode(node[childName], namesStack+[childName]))
        
        jsNode['children'] = children
        return jsNode

class Session(object):
    def __init__(self):
        self._clientConnections = []
        self._streamsTree = StreamsTree()
    
    def RegisterClientConnection(self, clientConnection):
        self._clientConnections.append(clientConnection)
        
    def UnRegisterClientConnection(self, clientConnection):
        self._clientConnections.remove(clientConnection)
        
    def ProcessZmqMessage(self, zmqMessage, rawStreamName):
        if self._streamsTree.IsEnabledStream(rawStreamName): 
            for clientConnection in self._clientConnections:
                clientConnection.write_message(zmqMessage)
            
    def GetStreamsTree(self):
        return self._streamsTree