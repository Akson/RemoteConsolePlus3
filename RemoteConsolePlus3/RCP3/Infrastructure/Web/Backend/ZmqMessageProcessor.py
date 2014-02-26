#Created by Dmytro Konobrytskyi, 2014 (github.com/Akson)
import json
from RCP3.Infrastructure.Web.Backend.StreamsCollector import StreamsCollector

class ZmqMessageProcessor(object):
    def __init__(self):
        self._streamsCollector = StreamsCollector()
        self._sessionClients = {}
        
    def OnIncomingZmqMessage(self, zmqMessages):
        for zmqMessage in zmqMessages:
            jsonMessage = json.loads(zmqMessage)
            streamName = jsonMessage["Stream"]
            self._streamsCollector.RegisterStreamName(streamName)

            for session in self._sessionClients:             
                for client in self._sessionClients[session]:
                    client.write_message(zmqMessage)
    
    def RegisterStreamListener(self, sessionName, streamListener):
        if not sessionName in self._sessionClients:
            self._sessionClients[sessionName] = []
        self._sessionClients[sessionName].append(streamListener)
        
    def UnRegisterStreamListener(self, sessionName, streamListener):
        self._sessionClients[sessionName].remove(streamListener)
