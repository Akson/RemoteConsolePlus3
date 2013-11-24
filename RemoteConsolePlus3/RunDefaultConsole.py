#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import wx
import logging
from RCP3.RCPCanvas import RCPCanvas

class CanvasWindow(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, size=[1280, 720], *args, **kw)
        s = wx.BoxSizer(wx.VERTICAL)
        
        canvas = RCPCanvas(self)
        canvas.CreateNodeFromDescriptionAtPosition('{"NodeClass": "SourceBackendNode", "APPLICATION_ID": "RemoteConsolePlus3", "NodeParameters":{"backendPath": "MoveMe.Canvas.Objects.MessageProcessingNodes.BackendObjectExample.PassThroughBackendObject"}}', [20,20])
        canvas.CreateNodeFromDescriptionAtPosition('{"NodeClass": "BackendNode", "APPLICATION_ID": "RemoteConsolePlus3"}', [240,20])
        canvas.CreateNodeFromDescriptionAtPosition('{"NodeClass": "DestinationBackendNode", "APPLICATION_ID": "RemoteConsolePlus3"}', [460,20])

        s.Add(canvas, 1, wx.EXPAND)
        self.SetSizer(s)
        self.SetTitle("Remote Console Plus 3 (RCP3) - Default Console")

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    app = wx.PySimpleApp()
    CanvasWindow(None).Show()
    app.MainLoop()