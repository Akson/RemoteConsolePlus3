#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import logging
import json
import struct
import numpy as np

def ParseBinaryData(binaryData, binaryDataFormat, dimensions):
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

def ParseDimensionsString(dimensionsString):
    dimensionsString = dimensionsString.lower()
    dimensionsString = dimensionsString.replace("(", "")
    dimensionsString = dimensionsString.replace(")", "")
    dimensionsString = dimensionsString.replace("[", "")
    dimensionsString = dimensionsString.replace("]", "")
    dimensionsString = dimensionsString.replace(" ", "")
    dimensionsString = dimensionsString.replace("x", ",")
    dimensionsString = dimensionsString.replace(";", ",")
    dimensions = [int(ds) for ds in dimensionsString.split(",")]
    return dimensions

def ParseMessage(message):
    processedMessage = dict()
    processedMessage["Stream"] = message["Stream"] 
    processedMessage["Info"] = message["Info"]
    
    #Parse data based on format. String is a default format
    dataType = message["Info"].get("DataType", "String")

    if dataType == "String":
        processedMessage["Data"] = message["Data"]

    if dataType == "JSON":
        jsonObj = json.loads(message["Data"])
        processedMessage["Data"] = jsonObj.get("_Value", jsonObj) 
    
    if dataType == "Binary":
        if not "BinaryDataFormat" in message["Info"]:
            logging.warning("Cannot parse binary data, no format data available")
            return None
        binaryDataFormat = message["Info"]["BinaryDataFormat"]
        
        #We may have multi-dimensional data
        dimensions = None
        if "Dimensions" in message["Info"]:
            dimensions = ParseDimensionsString(message["Info"]["Dimensions"])

        processedMessage["Data"] = ParseBinaryData(message["Data"], binaryDataFormat, dimensions)
    
    return processedMessage
