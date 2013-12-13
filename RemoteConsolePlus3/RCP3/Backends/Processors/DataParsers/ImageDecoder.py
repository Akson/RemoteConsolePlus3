#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import cv2
import numpy as np

class Backend(object):
    def __init__(self, parentNode):
        self._parentNode = parentNode

    def Delete(self):
        """
        This method is called when a parent node is deleted.
        """
        pass
    
    def GetParameters(self):
        """
        Returns a dictionary with object parameters, their values, 
        limits and ways to change them.
        """
        return {}
    
    def SetParameters(self, parameters):
        """
        Gets a dictionary with parameter values and
        update object parameters accordingly
        """
        pass
    
    def ProcessMessage(self, message):
        """
        This message is called when a new message comes. 
        If an incoming message should be processed by following nodes, the 
        'self._parentNode.SendMessage(message)'
        should be called with an appropriate message.
        """

        processedMessage = {"Stream":message["Stream"], "Info":message["Info"]} 

        if (not "Width" in message["Info"]) or (not "Height" in message["Info"]):
            #Try to decode image in one of standard formats
            img = cv2.imdecode(np.frombuffer(message["Data"], dtype=np.uint8), -1)
        else:
            w = int(message["Info"]["Width"])
            h = int(message["Info"]["Height"])
            BytesPerPixel = int(message["Info"]["BytesPerPixel"])
            LineSizeInBytes = int(message["Info"].get("LineSizeInBytes", w*BytesPerPixel))
            
            if LineSizeInBytes != w*BytesPerPixel:
                #We have padding bytes...
                print w, h, BytesPerPixel, LineSizeInBytes
                print "Not implemented!!!"
                processedMessage["Data"] = None
            else:
                img = np.reshape(message["Data"], (h, w, BytesPerPixel))
                cv2.imwrite("test.jpg", img)
                processedMessage["Data"] = img

        if img:            
            processedMessage["Data"] = img
            self._parentNode.SendMessage(processedMessage)
            
    def AppendContextMenuItems(self, menu):
        """
        Append backend specific menu items to a context menu that user will see
        when he clicks on a node.
        """
        pass