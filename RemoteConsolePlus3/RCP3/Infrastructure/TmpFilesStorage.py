#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
from RCP3.Configuration import Config
import uuid
import socket
import os


def NewTemporaryFile(extension = "tmp"):
    tmpFilesFolder = Config["Web server"]["Temporary files folder"]
    
    if not os.path.exists(tmpFilesFolder):
        os.makedirs(tmpFilesFolder)
    
    fileName = "tmp_{0}.{1}".format(str(uuid.uuid4()), extension)
    filePath = tmpFilesFolder + fileName
    link = "{}:{}/Tmp/{}".format(socket.gethostname(), Config["Web server"]["Port"], fileName)
    return (filePath, link)