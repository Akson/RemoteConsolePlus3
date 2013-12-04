#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import re

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
        
        processedMessage = dict(message)
        
        stream = message["Stream"]
        if stream.find("MatrixPrinter") == 0:
            components = stream.split("/")
            
            if len(components)>1:
                formatDescriptionString = components[-1]
                if formatDescriptionString[0] == "#":
                    formatDescriptionString = formatDescriptionString[1:]
                    #find the last digit and split stream name around it
                    reResult = re.search("\d", formatDescriptionString[::-1])
                    p = len(formatDescriptionString) - reResult.start() 
                    
                    processedMessage["Info"]["Dimensions"] = formatDescriptionString[:p] 
                    processedMessage["Info"]["BinaryDataFormat"] = formatDescriptionString[p:] 
        
        self._parentNode.SendMessage(processedMessage)
        
    def AppendContextMenuItems(self, menu):
        """
        Append backend specific menu items to a context menu that user will see
        when he clicks on a node.
        """
        pass