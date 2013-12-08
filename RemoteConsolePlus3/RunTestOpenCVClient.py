'''Created by Dmytro Konobrytskyi, 2013(C)'''

import zmq
import json
import time
import cv2

class RCP2Client(object):
    def __init__(self):
        pass
    
    def Connect(self, address):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.PUB)
        self._socket.connect(address)
    
    def SendMessage(self, value, streamName="TextHtml", additionalInfo={}):
        if streamName:
            if streamName[0] == "@":
                streamName = streamName[1:]
            else:
                if streamName != "TextHtml":
                    streamName += "TextHtml/"+streamName  
        
        if self._socket == None:
            raise Exception("Attempt to send message without connection.")

        additionalInfo["TimeStamp"] = int(time.time()*1000)
        
        message = "%s%c%s%c%s"%("" if streamName == None else streamName, chr(0), json.dumps(additionalInfo), chr(0), str(value))
    
        self._socket.send(message)

import numpy as np

if __name__ == '__main__':
    print "Running test client..."
    rc = RCP2Client()
    rc.Connect("tcp://127.0.0.1:55557")

    capture = cv2.VideoCapture(0)
    
    i=0
    while True:
        ret, frame = capture.read()
        if ret == False:
            print "No camera"
            time.sleep(1.0)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width = frame.shape[:2]
        print frame.dtype, frame.shape

        rc.SendMessage("Sending image...")
        info = {"DataType":"Binary", "BinaryDataFormat":"B", "Dimensions":str(frame.shape)}
        rc.SendMessage(json.dumps({"Value":info}), "TextHtml", {"DataType":"JSON"})
        #rc.SendMessage(frame.tostring(), "@ImageViewer", info)

        info = {"DataType":"IMAGE", "Dimensions":str(frame.shape)}
        ret, buf = cv2.imencode(".jpg", frame)
        print buf.shape
        bufStr = buf.tostring()
        rc.SendMessage(buf.tostring(), "@ImageViewer", info)

        i+=1
        time.sleep(1.5)