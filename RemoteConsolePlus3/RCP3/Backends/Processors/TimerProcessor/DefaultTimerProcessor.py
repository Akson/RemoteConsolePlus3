#Created by Dmytro Konobrytskyi, 2014 (github.com/Akson)

class EventData(object):
    lastValueMs = 0
    def __init__(self):
        pass
    
    def UpdateValueAndReturnDelta(self, value):
        oldVal = self.lastValueMs
        self.lastValueMs = value
        return value-oldVal

class TimerData(object):
    events = {}
    def __init__(self):
        pass

timersStorage = {}

def Ms2Html(ms):
    if ms < 10000:
        timeStr = "{0:> 8.3f}ms".format(ms)
    else:
        timeStr = "{0:> 8.3f}s".format(ms/1000.0)
    return timeStr.replace(" ", "&nbsp;")
    

def ParseMessage(message):
    processedMessage = dict()
    processedMessage["Stream"] = message["Stream"]
    processedMessage["Info"] = message["Info"]
    
    timerName = message["Info"]["TimerName"]
    if timerName not in timersStorage:
        timersStorage[timerName] = TimerData()   
    timerData = timersStorage[timerName]
    
    eventName = message["Info"]["EventName"]
    if eventName not in timerData.events:
        timerData.events[eventName] = EventData()
    eventData = timerData.events[eventName]
    
    timeMs = message["Data"]
    print eventData.lastValueMs
    deltaMs = eventData.UpdateValueAndReturnDelta(timeMs)
    print eventData.lastValueMs
    
    processedMessage["Data"] = "[Timer: {0}] {1} &Delta;={2} ({3})".format(timerName, Ms2Html(timeMs), Ms2Html(deltaMs), eventName)

    return processedMessage
