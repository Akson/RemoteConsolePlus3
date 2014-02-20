#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)

from RCP3.Infrastructure import WebSocketServer
from threading import Thread
import wx
import logging
from RCP3.MessageProcessingGraphWindow import MessageProcessingGraphWindow
import RCP3.Configuration
import multiprocessing.queues
from RCP3.Infrastructure.StreamsCollector import StreamsCollector

if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
    
    streamCollector = StreamsCollector("tcp://localhost:55557")
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