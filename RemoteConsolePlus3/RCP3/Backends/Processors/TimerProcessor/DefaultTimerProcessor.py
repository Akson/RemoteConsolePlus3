#Created by Dmytro Konobrytskyi, 2014 (github.com/Akson)
import math

class TimerData(object):
    def __init__(self):
        self.lastValueMs = 0

    def UpdateEventValueAndReturnDelta(self, eventName, value):
        oldVal = self.lastValueMs
        self.lastValueMs = value
        return value-oldVal

timersStorage = {}

def Ms2Html(ms):
    if ms < 10000:
        timeStr = "{0:>.3f}ms".format(ms)
    else:
        timeStr = "{0:>.3f}s".format(ms/1000.0)
    return timeStr.replace(" ", "&nbsp;")
    

def ParseMessage(message):
    processedMessage = dict()
    processedMessage["Stream"] = message["Stream"]
    processedMessage["Info"] = message["Info"]

    timerData = message["Data"]

    if len(timerData["Events"]) > 1:
        html = '<table border="1" style="display:inline-block">'
        html+= '<caption>{0} ({1})</caption>'.format(timerData["Timer name"], Ms2Html(timerData["Total time"]))
        lastTimeMs = 0
        for event in timerData["Events"]:
            html += '<tr><td>{0}</td><td align="right">{1}</td><td align="right">{2}</td></tr>'.format(event["Name"], Ms2Html(event["Time"]), Ms2Html(event["Time"]-lastTimeMs))
            lastTimeMs = event["Time"] 
        html += '</table>'
        
    else:
        event = timerData["Events"][0]
        html = "[TIMER {0}] {1} <b>{2}</b>".format(timerData["Timer name"], event["Name"], Ms2Html(event["Time"]))
    
    processedMessage["Data"] = html
    return processedMessage
