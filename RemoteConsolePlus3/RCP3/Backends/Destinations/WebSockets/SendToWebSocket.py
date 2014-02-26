#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
from RCP3.Infrastructure import WebSocketServer
import json
import wx
import webbrowser
from RCP3.Configuration import Config
import zmq

class Backend(object):
    def __init__(self, parentNode):
        self._parentNode = parentNode
        self._streamName = "DefaultConsole"
        
        self._outcomingSocket = zmq.Context.instance().socket(zmq.PUB)
        self._outcomingSocket.connect("tcp://localhost:"+str(Config["Web server"]["IncomingZmqPort"]))
        
    def GetParameters(self):
        """
        Returns a dictionary with object parameters, their values, 
        limits and ways to change them.
        """
        return {"StreamName":self._streamName}
    
    def SetParameters(self, parameters):
        """
        Gets a dictionary with parameter values and
        update object parameters accordingly
        """
        if "StreamName" in parameters:
            self._streamName = parameters["StreamName"]
    
    def ProcessMessage(self, message):
        """
        This message is called when a new message comes. 
        If an incoming message should be processed by following nodes, the 
        'self._parentNode.SendMessage(message)'
        should be called with an appropriate message.
        """
        self._outcomingSocket.send(json.dumps(message))

    def Delete(self):
        """
        This method is called when a parent node is deleted.
        """
        pass

    def OnOpenConsoleInBrowser(self, evt):
        linkDict = {}
        linkDict["serverAddress"]=Config["Web server"]["Address"]
        linkDict["serverPort"]=Config["Web server"]["Port"]
        linkDict["sessionName"]=self._streamName

        link = "http://{serverAddress}:{serverPort}/OutputConsole/?sessionName={sessionName}".format(**linkDict)
        webbrowser.open(link)

    def AppendContextMenuItems(self, menu):
        item = wx.MenuItem(menu, wx.NewId(), "Open console in browser")
        menu.Bind(wx.EVT_MENU, self.OnOpenConsoleInBrowser, item)
        menu.AppendItem(item)
