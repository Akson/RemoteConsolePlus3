#Created by Dmytro Konobrytskyi, 2014 (github.com/Akson)
from RCP3.Infrastructure.StreamsCollector import StreamsCollector
import json

class ZmqMessageProcessor(object):
    def __init__(self):
        self._streamsCollector = StreamsCollector()
        self._clientsConnectedToStreams = {}
        
    def OnIncomingZmqMessage(self, zmqMessages):
        for zmqMessage in zmqMessages:
            jsonMessage = json.loads(zmqMessage)
            streamName = jsonMessage["Stream"]
            self._streamsCollector.RegisterStreamName(streamName)

            for session in self._clientsConnectedToStreams:             
                for client in self._clientsConnectedToStreams[session]:
                    client.write_message(zmqMessage)
    
    def RegisterStreamListener(self, sessionName, streamListener):
        if not sessionName in self._clientsConnectedToStreams:
            self._clientsConnectedToStreams[sessionName] = []
        self._clientsConnectedToStreams[sessionName].append(streamListener)
        
    def UnRegisterStreamListener(self, sessionName, streamListener):
        self._clientsConnectedToStreams[sessionName].remove(streamListener)
