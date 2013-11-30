#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import wx
import logging
from RCP3.MessageProcessingGraphWindow import MessageProcessingGraphWindow

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    app = wx.PySimpleApp()

    mpgWindow = MessageProcessingGraphWindow()
    canvas = mpgWindow.canvas
    
    source = canvas.CreateNodeFromDescriptionAtPosition('{"NodeClass": "SourceBackendNode", "APPLICATION_ID": "RemoteConsole+ v3", "NodeParameters":{"backendPath": "RCP3.Backends.Sources.ZMQ.RcpStream", "backendParameters":{"serverAddress":"tcp://localhost:55559", "streamsList":[""]}}}', [20,20])
    processor = canvas.CreateNodeFromDescriptionAtPosition('{"NodeClass": "BackendNode", "APPLICATION_ID": "RemoteConsole+ v3", "NodeParameters":{"backendPath": "MoveMe.Canvas.Objects.MessageProcessingNodes.PassThroughBackendExample"}}', [240,20])
    destination = canvas.CreateNodeFromDescriptionAtPosition('{"NodeClass": "DestinationBackendNode", "APPLICATION_ID": "RemoteConsole+ v3", "NodeParameters":{"backendPath": "RCP3.Backends.Destinations.HtmlConsole.PyWxHtmlConsole"}}', [460,20])
    canvas.ConnectNodes(source, processor)
    canvas.ConnectNodes(processor, destination)

    app.MainLoop()