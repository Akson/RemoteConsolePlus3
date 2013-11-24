#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
from MoveMe.Canvas.Canvas import Canvas
from MoveMe.Canvas.Factories.DefaultNodesFactory import DefaultNodesFactory
from MoveMe.Canvas.Objects.MessageProcessingNodes.BackendNode import SourceBackendNode,\
    BackendNode, DestinationBackendNode

class RCPCanvas(Canvas):
    def __init__(self, parent):
        supportedClasses = {
                   "SourceBackendNode":SourceBackendNode, 
                   "BackendNode":BackendNode, 
                   "DestinationBackendNode":DestinationBackendNode 
                   } 
        super(RCPCanvas, self).__init__(parent=parent, nodesFactory=DefaultNodesFactory(supportedClasses))
        self.applicationId = "RemoteConsolePlus3"