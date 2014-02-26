'''Created by Dmytro Konobrytskyi, 2013(C)'''

import zmq
import time

import collections
import json
import traceback

def Tree():
    return collections.defaultdict(Tree)

class StreamsCollector(object):
    def __init__(self):
        self._root = Tree()

    def GetStreamsTree(self):
        return self._root

    def RegisterStreamName(self, rawStreamName):
        print rawStreamName
        streamName = rawStreamName[:-1]
        streamComponents = streamName.split("/")
        curNode = self._root
        for component in streamComponents:
            if component not in curNode:
                curNode[component] = Tree()
            curNode = curNode[component]
