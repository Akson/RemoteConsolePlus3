#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import wx
from MoveMe.Canvas.Objects.MessageProcessingNodes.BackendNode import SourceBackendNode,\
    BackendNode, DestinationBackendNode
from MoveMe.Canvas.Canvas import Canvas
from MoveMe.Canvas.Factories.DefaultNodesFactory import DefaultNodesFactory
from RCP3.CommonUIRoutines import ConfirmApplicationExit
from RCP3.OutputWindowsContainer import OutputWindowsContainer
from RCP3.Configuration import Config
import json
import os.path

class RCPCanvas(Canvas):
    def __init__(self, parent):
        self.supportedClassesList =[SourceBackendNode, BackendNode, DestinationBackendNode]
        super(RCPCanvas, self).__init__(parent=parent, nodesFactory=DefaultNodesFactory(self.supportedClassesList))
        self.applicationId = Config["Application ID"]
        
    def LoadCanvasFromDict(self, canvasDict):
        OutputWindowsContainer.CreateNewOutputWindowsContainer()
        super(RCPCanvas, self).LoadCanvasFromDict(canvasDict)
        
    def AppendContextMenuItems(self, parentMenu):
        if not self._objectUnderCursor:#We don't want to add a node on top of another node
            newElementMenu = wx.Menu()
            parentMenu.AppendSubMenu(newElementMenu, "New node")
            
            menuItemId2ClassNameMap = {}
            for nodeClass in self.supportedClassesList:
                iid = wx.NewId()
                menuItemId2ClassNameMap[iid] = nodeClass.__name__
                item = wx.MenuItem(newElementMenu, iid, "%s (%s)"%(nodeClass.shortHumanFriendlyDescription, nodeClass.__name__))
                newElementMenu.AppendItem(item)
                parentMenu.Bind(wx.EVT_MENU, (lambda evt: self.OnNewNode(evt, menuItemId2ClassNameMap)), item)
        
    def OnNewNode(self, event, menuItemId2ClassNameMap):
        nodeDescriptionDict = {}
        nodeDescriptionDict["APPLICATION_ID"] = self.applicationId
        nodeDescriptionDict["NodeClass"] = menuItemId2ClassNameMap[event.GetId()]
        self.CreateNodeFromDescriptionAtPosition(nodeDescriptionDict, self._mousePositionAtContextMenuCreation)
        


class MessageProcessingGraphWindow(wx.Frame):
    def __init__(self, *args, **kw):
        wx.Frame.__init__(self, parent=None, title="RemoteConsole+ message processing graph", size=[800, 600], *args, **kw)
        OutputWindowsContainer.Instance(self)
        self.InitializeMenuBar()

        self.canvas = RCPCanvas(self)
        s = wx.BoxSizer(wx.VERTICAL)
        s.Add(self.canvas, 1, wx.EXPAND)
        self.SetSizer(s)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        if Config["UI behavior"]["Show message processing graph on start"]:
            self.Show() 
        
    def InitializeMenuBar(self):
        mb = wx.MenuBar()

        menu = wx.Menu()
        self.Bind(wx.EVT_MENU, self.OnLoadMessageProcessingGraph, menu.Append(wx.NewId(), "Load message processing graph"))
        self.Bind(wx.EVT_MENU, self.OnSaveMessageProcessingGraph, menu.Append(wx.NewId(), "Save message processing graph"))
        mb.Append(menu, "Processing graph")

        menu = wx.Menu()
        self.Bind(wx.EVT_MENU, (lambda event: [OutputWindowsContainer.Instance().Show(), OutputWindowsContainer.Instance().Raise()]), menu.Append(wx.NewId(), "Show output windows"))
        mb.Append(menu, "Output windows")

        self.SetMenuBar(mb)

    def OnLoadMessageProcessingGraph(self, evt):
        dlg = wx.FileDialog(self, "Choose a file", '', "", "RemoteConsole+ files (*.rcp)|*.rcp", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.LoadFile(os.path.join(dlg.GetDirectory(), dlg.GetFilename()))
        dlg.Destroy()
        
    def OnSaveMessageProcessingGraph(self, evt):
        dlg = wx.FileDialog(self, "Choose a file", '', "", "RemoteConsole+ files (*.rcp)|*.rcp", wx.SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.SaveFile(os.path.join(dlg.GetDirectory(), dlg.GetFilename()))
        dlg.Destroy()

    def SaveFile(self, fileName):
        f = open(fileName, 'w')
        fileDict = {}
        fileDict["File format version"] = 1
        fileDict["RCPCanvas"] = self.canvas.SaveCanvasToDict() 
        f.write(json.dumps(fileDict, sort_keys=True, indent=4, separators=(',', ': ')))
        f.close()

    def LoadFile(self, fileName):
        f = open(fileName, 'r')
        fileDict = json.load(f)
        self.canvas.LoadCanvasFromDict(fileDict["RCPCanvas"])
        f.close()

    def OnClose(self, event):
        if OutputWindowsContainer.Instance().IsShown():
            self.Hide()
        else:
            ConfirmApplicationExit(self, OutputWindowsContainer.Instance())      