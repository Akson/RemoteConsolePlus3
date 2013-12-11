#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
from RCP3.Infrastructure import WebSocketServer
import json
import wx
import webbrowser
import socket
from RCP3.Configuration import Config

class Backend(object):
    def __init__(self, parentNode):
        self._parentNode = parentNode
        self._streamName = "DefaultConsole"
    
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
        WebSocketServer.proxyQueue.put(json.dumps({"StreamName":self._streamName, "Message":str(message["Data"])}))

    def Delete(self):
        """
        This method is called when a parent node is deleted.
        """
        pass

    def OnOpenConsoleInBrowser(self, evt):
        linkDict = {}
        linkDict["serverAddress"]=socket.gethostname()
        linkDict["serverPort"]=Config["Web server"]["Port"]
        linkDict["streamName"]=self._streamName

        link = "http://{serverAddress}:{serverPort}/OutputConsole/?streamName={streamName}".format(**linkDict)
        webbrowser.open(link)

    def AppendContextMenuItems(self, menu):
        item = wx.MenuItem(menu, wx.NewId(), "Open console in browser")
        menu.Bind(wx.EVT_MENU, self.OnOpenConsoleInBrowser, item)
        menu.AppendItem(item)
