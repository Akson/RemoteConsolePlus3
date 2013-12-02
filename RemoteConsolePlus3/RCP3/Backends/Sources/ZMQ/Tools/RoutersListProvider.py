#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import time

serversList = ["tcp://localhost:55559", 'CET', 'GMT', 'MSK', 'EST', 'PST', 'EST', 'PST', 'EDT', 'EDT', 'EDT', str(time.time())]

def GetAvailableRoutersList():
    serversList.append(str(time.time()))
    return serversList