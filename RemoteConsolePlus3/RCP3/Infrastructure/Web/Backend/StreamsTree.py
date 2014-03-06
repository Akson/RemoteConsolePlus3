#Created by Dmytro Konobrytskyi, 2014 (github.com/Akson)

class StreamsTreeNode(dict):
    def __init__(self):
        self._selected = True
        
class StreamsTree(object):
    def __init__(self):
        self._root = StreamsTreeNode()
        
    def FindStreamNode(self, rawStreamName):
        newNode = False
        streamName = rawStreamName[:-1]
        streamComponents = streamName.split("/")
        curNode = self._root
        for component in streamComponents:
            if component not in curNode:
                curNode[component] = StreamsTreeNode()
                newNode = True
            curNode = curNode[component]
        
        return (newNode, curNode._selected)

    def GetTreeInJstreeFormat(self):
        #self.PrintSubtree([self._root])
        return [self.ConvertStreamsTreeNodeIntoJstreeNode(self._root[childName], [childName]) for childName in self._root]

    def ConvertStreamsTreeNodeIntoJstreeNode(self, node, namesStack):
        jsNode = {}
        jsNode['text'] = namesStack[-1]
        jsNode['id'] = "/".join(namesStack)
        jsNode['children'] = []

        if len(node) == 0:
            jsNode['state'] = {'selected':node._selected}
        else:
            localRootNode = {}
            localRootNode['id'] = "/".join(namesStack)
            localRootNode['text'] = '.'
            localRootNode['state'] = {'selected':node._selected}
            jsNode['id'] += "#"
            if namesStack[-1] != "ROOT":
                jsNode['children'].append(localRootNode)

            for childName in node:
                jsNode['children'].append(self.ConvertStreamsTreeNodeIntoJstreeNode(node[childName], namesStack+[childName]))
        
        return jsNode
    
    def ClearSelectionRecursively(self, node):
        node._selected = False
        for childName in node:
            self.ClearSelectionRecursively(node[childName])
    
    def UpdateSelectionFromList(self, selectedNodes):
        self.ClearSelectionRecursively(self._root)
        
        for selectedNodeId in selectedNodes:
            if selectedNodeId[-1] == '#':
                continue
            pathComponents = selectedNodeId.split("/")
            print pathComponents

            curNode = self._root
            for component in pathComponents:
                curNode = curNode[component]
            
            curNode._selected = True
            
        #self.PrintSubtree([self._root])

    def PrintSubtree(self, nodesStack):
        curNode = nodesStack[-1]
        for childName in curNode:
            print '    '*(len(nodesStack)-1), childName, curNode[childName]._selected
            self.PrintSubtree(nodesStack+[curNode[childName]]) 

    def ClearTree(self):
        self._root = StreamsTreeNode()