#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import logging
import json
import struct
import numpy as np
import traceback

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
    
    def ParseBinaryData(self, binaryData, binaryDataFormat, dimensions):
        elementSize = struct.calcsize(binaryDataFormat)
        elementsNumber = len(binaryData) / elementSize
        
        #Single element case
        if elementsNumber == 1:
            return struct.unpack(binaryDataFormat, binaryData)[0]

        #It looks like we have an array, parse it with NumPy
        if dimensions == None:
            return np.frombuffer(binaryData, binaryDataFormat)
        
        #And it is actually a multi-dimensional array
        return np.ndarray(shape=dimensions, dtype=binaryDataFormat, buffer=binaryData)
    
    def ParseDimensionsString(self, dimensionsString):
        dimensionsString = dimensionsString.lower()
        dimensionsString = dimensionsString.replace(" ", "")
        dimensionsString = dimensionsString.replace("x", ",")
        dimensionsString = dimensionsString.replace(";", ",")
        dimensions = [int(ds) for ds in dimensionsString.split(",")]
        return dimensions
    
    def ProcessMessage(self, message):
        """
        This message is called when a new message comes. 
        If an incoming message should be processed by following nodes, the 
        'self._parentNode.SendMessage(message)'
        should be called with an appropriate message.
        """
        
        processedMessage = dict()
        processedMessage["Stream"] = message["Stream"] 
        processedMessage["Info"] = message["Info"]
        
        #Parse data based on format. String is a default format
        dataType = message["Info"].get("DataType", "String")

        if dataType == "String":
            processedMessage["Data"] = message["Data"]

        if dataType == "JSON":
            processedMessage["Data"] = json.loads(message["Data"])["Value"]
        
        if dataType == "Binary":
            if not "BinaryDataFormat" in message["Info"]:
                logging.warning("Cannot parse binary data, no format data available")
                return
            binaryData = message["Data"]
            binaryDataFormat = message["Info"]["BinaryDataFormat"]
            #We may have multi-dimensional data
            dimensions = None
            if "Dimensions" in message["Info"]:
                dimensions = self.ParseDimensionsString(message["Info"]["Dimensions"])
            processedMessage["Data"] = self.ParseBinaryData(binaryData, binaryDataFormat, dimensions)

        self._parentNode.SendMessage(processedMessage)
        
    def AppendContextMenuItems(self, menu):
        """
        Append backend specific menu items to a context menu that user will see
        when he clicks on a node.
        """
        pass