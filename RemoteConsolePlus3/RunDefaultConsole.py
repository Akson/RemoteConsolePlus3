#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)

import sys
import traceback
from multiprocessing import Process
from RCP3.Infrastructure import WebSocketServer
from threading import Thread
import subprocess
import wx
import logging
from RCP3.MessageProcessingGraphWindow import MessageProcessingGraphWindow
import RCP3.Configuration
import multiprocessing.queues
from RCP3.Infrastructure.StreamsCollector import StreamsCollector
from RCP3.Infrastructure.Router import Router
from zmq.error import ZMQError
import zmq

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    
    try:
        router = Router("tcp://*:55557", "tcp://*:55559")
    except ZMQError as e:
        if e.errno == zmq.EADDRINUSE:
            print "It looks like another router is already running. So we don't start this one."
        else:
            print traceback.format_exc()
            sys.exit(-1)
    p0 = Thread(target=Router.Run, args=(router,))
    p0.start()
        
    streamCollector = StreamsCollector("tcp://localhost:55559")
    p1 = Thread(target=StreamsCollector.Run, args=(streamCollector,))
    p1.start()

    WebSocketServer.proxyQueue = multiprocessing.queues.Queue(1024)
    p = Thread(target=WebSocketServer.Run, args=(WebSocketServer.proxyQueue, streamCollector,))
    p.start()
    
    app = wx.PySimpleApp()
    mpgWindow = MessageProcessingGraphWindow()
    mpgWindow.LoadFile("Default.rcp")
    app.MainLoop()
    RCP3.Configuration.SaveConfiguration()