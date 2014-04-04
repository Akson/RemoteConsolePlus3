#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)

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
        parsedMessage = ParseMessage(message)
        if parsedMessage:
            self._parentNode.SendMessage(parsedMessage)
        
    def AppendContextMenuItems(self, menu):
        """
        Append backend specific menu items to a context menu that user will see
        when he clicks on a node.
        """
        pass


    
class TimeRange(object):
    def __init__(self, name, endTime, childrenBlocks):
        self.endTime = endTime
        self.name = name
        self.childrenBlocks = childrenBlocks
            
def ParseBlockRecursively(listIter, blockName, blockStartTime):
    timeRanges = [TimeRange(blockName, blockStartTime, [])]
    blocksSinceLastTick = []
    while True:
        tickName, tickTime = next(listIter, ("_BLOCK_END_", 0))
        if tickName[:13] == "_BLOCK_START_":
            subBlock = ParseBlockRecursively(listIter, tickName, tickTime)
            blocksSinceLastTick.append(subBlock)
        elif tickName[:11] == "_BLOCK_END_":
            timeRanges.append(TimeRange(tickName, tickTime, blocksSinceLastTick))
            return timeRanges
        else:
            timeRanges.append(TimeRange(tickName, tickTime, blocksSinceLastTick))
            blocksSinceLastTick = []

def PrintRecursively(block, prefix):
    result = ""
    for tr in block:
        for cb in tr.childrenBlocks:
            result += PrintRecursively(cb, prefix+">>>")
        result += "{} {} {}\n".format(prefix, tr.endTime, tr.name)
    return result

def Ms2Html(ms):
    if ms < 10000:
        timeStr = "{0:>.3f}ms".format(ms)
    else:
        timeStr = "{0:>.3f}s".format(ms/1000.0)
    return timeStr.replace(" ", "&nbsp;")

def PrintHtmlTableRecursively(block):
    tableRows = ""
    if len(block) > 0:
        lastTimeMs = block[0].endTime
    for tr in block[1:-1]:
        for cb in tr.childrenBlocks:
            tableRows += '<tr>'
            tableRows += '<td colspan="3" style="padding-left:20px;">'
            tableRows += '<div class="timing-block-opener" onclick="$(this).next().slideToggle(100);"></div>'
            tableRows += '<table class="HttSubtable" border="1" width="100%">'
            tableRows += PrintHtmlTableRecursively(cb)
            tableRows += '</table>'
            tableRows += '</td></tr>'
        tableRows += '<tr><td>{}</td><td align="right">{}</td><td align="right">{}</td></tr>'.format(tr.name, Ms2Html(tr.endTime), Ms2Html(tr.endTime-lastTimeMs))
        lastTimeMs = tr.endTime 
    return tableRows

def ParseMessage(message):
    processedMessage = dict()
    processedMessage["Stream"] = message["Stream"]
    processedMessage["Info"] = message["Info"]

    ticks = [tick.items()[0] for tick in message["Data"]["Ticks"]]
    timeRanges = ParseBlockRecursively(iter(ticks), "HTT", 0)

    html = '<table border="1" style="display:inline-block">'
    html += PrintHtmlTableRecursively(timeRanges)
    html += '</table>'

    processedMessage["Data"] = html
    return processedMessage
