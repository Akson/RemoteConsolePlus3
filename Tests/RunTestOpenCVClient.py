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
    
    def SendMessage(self, value, streamName="", additionalInfo={"ProcessingSequence":"_Text"}):
        if self._socket == None:
            raise Exception("Attempt to send message without connection.")

        additionalInfo["TimeStamp"] = int(time.time()*1000)
        
        message = "%s#%c%s%c%s"%("DefaultStream" if streamName == None else streamName, chr(0), json.dumps(additionalInfo), chr(0), str(value))
    
        self._socket.send(message)

import numpy as np

if __name__ == '__main__':
    print "Running test client..."
    rc = RCP2Client()
    rc.Connect("tcp://localhost:55557")

    capture = cv2.VideoCapture(0)
    
    i=0
    while True:
        ret, frame = capture.read()
        if ret == False:
            print "No camera"
            time.sleep(1.0)
        height, width = frame.shape[:2]
        print frame.dtype, frame.shape

        rc.SendMessage("Sending image...", "Webcam")

        info = {"DataType":"Binary", "BinaryDataFormat":"B", "Dimensions":str(frame.shape)}
        rc.SendMessage(json.dumps({"Value":info}), "Webcam/Info", {"ProcessingSequence":"_Json", "DataType":"JSON"})

        ret, buf = cv2.imencode(".jpg", frame)
        rc.SendMessage(buf.tostring(), "Webcam/Image", {"ProcessingSequence":"_Image"})
        print ret, buf.shape

        i+=1
        time.sleep(1)