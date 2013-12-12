#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import zmq
import thread
import json
from RCP3.Configuration import Config
import wx
from RCP3.Backends.Sources.ZMQ.Tools.UI import ServerSelectionDialog,\
    StreamsSelectionDialog
import logging
import time
from RCP3 import DefaultParser


class Backend(object):
    def __init__(self, parentNode):
        self._parentNode = parentNode
        
        self._streamsList = []
        self._serverAddress = None

        self._listeningThreadRunning = False
        self._stopListening = False
        self._reconnectToServer = False

        self.threadStopWaitTimeMs = Config["Backends"]["Thread stop waiting time (ms)"]
        
        self.text = None
    
    def AppendContextMenuItems(self, menu):
        item = wx.MenuItem(menu, wx.NewId(), "Select router address")
        menu.Bind(wx.EVT_MENU, self.OnSelectServer, item)
        menu.AppendItem(item)
        
        if self._serverAddress:
            item = wx.MenuItem(menu, wx.NewId(), "Select streams")
            menu.Bind(wx.EVT_MENU, self.OnSelectStreams, item)
            menu.AppendItem(item)
        
    def OnSelectServer(self, evt):
        serverSelectionDialog = ServerSelectionDialog(self._serverAddress)
        serverSelectionDialog.ShowModal()
        serverSelectionDialog.Destroy()
        self.SetParameters({"serverAddress":serverSelectionDialog.serverAddress})
    
    def OnSelectStreams(self, evt):
        streamsSelectionDialog = StreamsSelectionDialog(self._serverAddress, self._streamsList)
        streamsSelectionDialog.ShowModal()
        streamsSelectionDialog.Destroy()
        self.SetParameters({"streamsList":streamsSelectionDialog.streamsList})

    def Delete(self):
        self._stopListening = True
    
    def GetParameters(self):
        return {"streamsList":self._streamsList, "serverAddress":self._serverAddress}
    
    def SetParameters(self, parameters):
        self._streamsList = parameters.get("streamsList", self._streamsList)
        self._serverAddress = parameters.get("serverAddress", self._serverAddress)
        
        if self._serverAddress!=None and len(self._streamsList)>0:
            self._reconnectToServer = True
            if not self._listeningThreadRunning:
                thread.start_new_thread(self.StreamListenerThreadFunc, ())
        
        self.text = str(self._streamsList)
        
    def StreamListenerThreadFunc(self):
        self._listeningThreadRunning = True
        
        while not self._stopListening:
            #Reconnect to server if needed
            if self._reconnectToServer:
                try:
                    socket = zmq.Context.instance().socket(zmq.SUB)
                    socket.connect(self._serverAddress)
                    for streamName in self._streamsList:
                        socket.setsockopt(zmq.SUBSCRIBE, str(streamName))
                    self._reconnectToServer = False
                except zmq.ZMQError, e:
                    logging.error("ZMQ cannot connect to the specified router address: "+self._serverAddress)
                    #If we cannot connect, just stop this thread
                    break

            #Wait for incoming messages 
            if socket.poll(self.threadStopWaitTimeMs) and not self._stopListening:
                try:
                    zmqMessage = socket.recv()
                except zmq.ZMQError, e:
                    print e
                self.ProcessIncomingZmqMessage(zmqMessage)
        
        self._listeningThreadRunning = False

    def ProcessIncomingZmqMessage(self, zmqMessage):
        """
        Incoming message format is:
        [Stream name string]0[Information in JSON format]0[Data]
        """
        parsedMessage = {}
        messageComponents = zmqMessage.split(chr(0), 2)
        parsedMessage["Stream"] = messageComponents[0]
        parsedMessage["Data"] = messageComponents[2]
        
        parsedMessage["Info"] = {}
        if messageComponents[1] != "":
            parsedMessage["Info"] = json.loads(messageComponents[1])
        parsedMessage["Info"]["ServerTimeStampMsSince1970"] = int(time.time()*1000)
        
        self._parentNode.SendMessage(parsedMessage)