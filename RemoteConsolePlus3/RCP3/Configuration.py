#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)

"""
RCP3Configuration stores configurations for the RCP application. 
All constants should be stored here. 
"""

Config = {}

Config["Application ID"] = "RemoteConsole+ v3"

Config["UI behavior"] = {}
Config["UI behavior"]["Ask before exit"] = False
Config["UI behavior"]["Show message processing graph on start"] = True

Config["Backends"] = {}
Config["Backends"]["Thread stop waiting time (ms)"] = 200