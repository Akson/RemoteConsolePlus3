#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)

import json
import logging
import traceback
import os
import socket

"""
Configuration stores configurations for the RCP application. 
All constants should be stored here.
It is initialized with default settings in this file and updated from a config file on start. 
"""

Config = {}

Config["Application ID"] = "RemoteConsole+ v3"

Config["UI behavior"] = {}
Config["UI behavior"]["Ask before exit"] = False

Config["UI behavior"]["Message processing graph window"] = {}
Config["UI behavior"]["Message processing graph window"]["Show on start"] = True
Config["UI behavior"]["Message processing graph window"]["Window position"] = [0, 0]
Config["UI behavior"]["Message processing graph window"]["Window size"] = [640, 480]

Config["UI behavior"]["Output windows container"] = {}
Config["UI behavior"]["Output windows container"]["Show on start"] = False
Config["UI behavior"]["Output windows container"]["Show after adding new window"] = False
Config["UI behavior"]["Output windows container"]["Window position"] = [0, 480]
Config["UI behavior"]["Output windows container"]["Window size"] = [640, 480]

Config["Backends"] = {}
Config["Backends"]["Thread stop waiting time (ms)"] = 200

Config["Web server"] = {}
Config["Web server"]["Address"] = socket.gethostname()
Config["Web server"]["Port"] = 55558
Config["Web server"]["Temporary files folder"] = os.getcwd()+"\\RCPTemp\\"

Config["ZMQ"] = {}
Config["ZMQ"]["Router input address"] = "*"
Config["ZMQ"]["Router input port"] = 55557
Config["ZMQ"]["Router output address"] = "*"
Config["ZMQ"]["Router output port"] = 55559


"""
Saving/Loading a configuration in/from file 
"""
ConfigurationFileName = "RCP3Config.json"

def UpdateDictTreeRecursively(source, destination):
    for key in source:
        if type(source[key]) == dict:
            UpdateDictTreeRecursively(source[key], destination[key])
        else:
            destination[key] = source[key]

def SaveConfiguration(fileName=ConfigurationFileName):
    try:
        f = open(fileName, 'w')
        f.write(json.dumps(Config, sort_keys=True, indent=4, separators=(',', ': ')))
        f.close()
    except:
        logging.warning("Cannot write configuration file: "+fileName)
        logging.debug(traceback.format_exc())
    
def LoadConfiguration(fileName=ConfigurationFileName):
    try:
        f = open(fileName, 'r')
        fileDictTree = json.load(f)
        UpdateDictTreeRecursively(fileDictTree, Config)
        f.close()
    except:
        logging.warning("Cannot read configuration file: "+fileName)
        logging.debug(traceback.format_exc())
    
LoadConfiguration()
