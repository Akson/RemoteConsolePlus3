#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import time

def GetAvailableRoutersList():
    return ["tcp://localhost:55559", 'CET', 'GMT', 'MSK', 'EST', 'PST', 'EDT', 'EDT', 'EDT', str(time.time())]