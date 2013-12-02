#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)

import sys
import traceback
sys.path.append('..\MoveMe')#MoveMe should live near RCP
import subprocess
import wx
import logging
from RCP3.MessageProcessingGraphWindow import MessageProcessingGraphWindow
import RCP3.Configuration

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    
    #We try to run a new router, if another router is already running, it will throw an exception but it's ok
    routerProcess = subprocess.Popen(['python', 'RunRouter.py'])
    
    try:
        app = wx.PySimpleApp()
    
        mpgWindow = MessageProcessingGraphWindow()
        canvas = mpgWindow.canvas
        
        source = canvas.CreateNodeFromDescriptionAtPosition('{"NodeClass": "SourceBackendNode", "APPLICATION_ID": "RemoteConsole+ v3", "NodeParameters":{"backendPath": "RCP3.Backends.Sources.ZMQ.RcpStream", "backendParameters":{"serverAddress":"tcp://localhost:55559", "streamsList":[""]}}}', [20,20])
        processor = canvas.CreateNodeFromDescriptionAtPosition('{"NodeClass": "BackendNode", "APPLICATION_ID": "RemoteConsole+ v3", "NodeParameters":{"backendPath": "MoveMe.Canvas.Objects.MessageProcessingNodes.PassThroughBackendExample"}}', [240,20])
        destination = canvas.CreateNodeFromDescriptionAtPosition('{"NodeClass": "DestinationBackendNode", "APPLICATION_ID": "RemoteConsole+ v3", "NodeParameters":{"backendPath": "RCP3.Backends.Destinations.HtmlConsole.PyWxHtmlConsole"}}', [460,20])
        canvas.ConnectNodes(source, processor)
        canvas.ConnectNodes(processor, destination)
        
        mpgWindow.LoadFile("Default.rcp")

        app.MainLoop()
        RCP3.Configuration.SaveConfiguration()
        
    except:
        print traceback.format_exc()
        
    #Stop the router
    routerProcess.kill()