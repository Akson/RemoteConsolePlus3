#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import cv2
from RCP3.Infrastructure import TmpFilesStorage
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
        
        filePath, link = TmpFilesStorage.NewTemporaryFile("jpg")
        print filePath
        print link
        cv2.imwrite(filePath, message["Data"])
        html = '<img src="http://{}" alt="Image should come here">'.format(link)
        processedMessage["Data"] = html
        
        print html
        
        self._parentNode.SendMessage(processedMessage)
        
    def AppendContextMenuItems(self, menu):
        """
        Append backend specific menu items to a context menu that user will see
        when he clicks on a node.
        """
        pass