#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import wx
from MoveMe.Canvas.Objects.MessageProcessingNodes.BackendNode import SourceBackendNode,\
    BackendNode, DestinationBackendNode
from MoveMe.Canvas.Canvas import Canvas
from MoveMe.Canvas.Factories.DefaultNodesFactory import DefaultNodesFactory
from RCP3.CommonUIRoutines import ConfirmApplicationExit
from RCP3.OutputWindowsContainer import OutputWindowsContainer

class RCPCanvas(Canvas):
    def __init__(self, parent):
        supportedClasses = {
                   "SourceBackendNode":SourceBackendNode, 
                   "BackendNode":BackendNode, 
                   "DestinationBackendNode":DestinationBackendNode 
                   } 
        super(RCPCanvas, self).__init__(parent=parent, nodesFactory=DefaultNodesFactory(supportedClasses))
        self.applicationId = "RemoteConsolePlus3"
        
    def LoadCanvasFromDict(self, canvasDict):
        OutputWindowsContainer.CreateNewOutputWindowsContainer()
        super(RCPCanvas, self).LoadCanvasFromDict(canvasDict)



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
        
    def InitializeMenuBar(self):
        outputWindowsMenu = wx.Menu()
        self.Bind(wx.EVT_MENU, (lambda event: OutputWindowsContainer.Instance().Show()), outputWindowsMenu.Append(wx.NewId(), "Show output windows"))

        mb = wx.MenuBar()
        mb.Append(outputWindowsMenu, "Output windows")
        self.SetMenuBar(mb)


    def OnClose(self, event):
        if OutputWindowsContainer.Instance().IsShown():
            self.Hide()
        else:
            ConfirmApplicationExit(self, OutputWindowsContainer.Instance())      