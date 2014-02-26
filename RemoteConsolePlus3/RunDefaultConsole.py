#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)

from threading import Thread
import wx
import logging
from RCP3.MessageProcessingGraphWindow import MessageProcessingGraphWindow
import RCP3.Configuration
from RCP3.Infrastructure.Web.Backend import WebSocketServer

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    
    webserverThread = Thread(target=WebSocketServer.Run)
    webserverThread.start()
    
    app = wx.PySimpleApp()
    mpgWindow = MessageProcessingGraphWindow()
    mpgWindow.LoadFile("Default.rcp")
    
    app.MainLoop()
    
    WebSocketServer.WebServerStopRequested = True
    RCP3.Configuration.SaveConfiguration()
    webserverThread.join()