#Created by Dmytro Konobrytskyi, 2014 (github.com/Akson)
import json
from RCP3.Infrastructure.Web.Backend.Session import Session

class SessionsManager(object):
    def __init__(self):
        self._sessions = {"_ZERO_SESSION":Session()}
    
    def ProcessZmqMessages(self, zmqMessages):
        for zmqMessage in zmqMessages:
            jsonMessage = json.loads(zmqMessage)
            rawStreamName = jsonMessage["Stream"]
            print rawStreamName
            
            for session in self._sessions.itervalues():
                session.ProcessZmqMessage(zmqMessage, rawStreamName)

    def RegisterClientConnection(self, sessionId, clientConnection):
        if sessionId not in self._sessions:
            self._sessions[sessionId] = Session()
        
        self._sessions[sessionId].RegisterClientConnection(clientConnection)
    
    def UnRegisterClientConnection(self, sessionId, clientConnection):
        self._sessions[sessionId].UnRegisterClientConnection(clientConnection)
    
    def GetSessionTree(self, sessionId):
        return self._sessions[sessionId].GetStreamsTree()