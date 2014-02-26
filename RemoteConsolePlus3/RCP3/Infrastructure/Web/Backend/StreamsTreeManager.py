#Created by Dmytro Konobrytskyi, 2014 (github.com/Akson)

import tornado
import json
from random import randint, random

class StreamsTreeRequestHandler(tornado.web.RequestHandler):
    _currentTree = {'text':'root', 'children':[], 'id':'root'}

    def initialize(self, zmqMessageProcessor):
        self._zmqMessageProcessor = zmqMessageProcessor
        
    def CreateNewRandomTreeNode(self):
        rnadStr = 'node'+str(randint(0, 10000))
        return {'text':rnadStr, 'children':[], 'id':rnadStr}

    def GrowTree(self, newNodesNumber = 1):
        for i in range(newNodesNumber):
            curNode = StreamsTreeRequestHandler._currentTree
            while len(curNode['children']) > 0:
                if random()<(1.0/len(curNode['children'])):
                    break
                curNode = curNode['children'][randint(0, len(curNode['children'])-1)]
            curNode['children'].append(self.CreateNewRandomTreeNode())
    
    @tornado.web.asynchronous
    def get(self, params):
        print "tree requested", params
        self.GrowTree(10)
        self.set_header("Content-Type", 'application/json')
        self.write(json.dumps(StreamsTreeRequestHandler._currentTree))
        print json.dumps(StreamsTreeRequestHandler._currentTree)
        self.flush()
        self.finish()