'''Created by Dmytro Konobrytskyi, 2012(C)'''
import wx
from wx.lib.agw import aui
from RCP3.CommonUIRoutines import ConfirmApplicationExit
from RCP3.Configuration import Config

class OutputWindowsContainer(wx.Frame):
    '''
    This is a main window that may have multiple subwindows managed by AuiManager.
    These subwindows will contain output of destination nodes.
    '''
    _instance = None
    @staticmethod
    def Instance(messageProcessingGraphWindow=None):
        if OutputWindowsContainer._instance == None:
            OutputWindowsContainer._instance = OutputWindowsContainer(messageProcessingGraphWindow)
        return OutputWindowsContainer._instance
    
    @staticmethod
    def CreateNewOutputWindowsContainer():
        oldWindow = OutputWindowsContainer._instance
        OutputWindowsContainer._instance = OutputWindowsContainer(oldWindow.messageProcessingGraphWindow)
        oldWindow.Destroy()
        OutputWindowsContainer.Instance().Show()

    
    
    def __init__(self, messageProcessingGraphWindow):
        wx.Frame.__init__(self, 
                          None, 
                          id=wx.ID_ANY, 
                          title="RemoteConsole+ output windows", 
                          size=Config["UI behavior"]["Output windows container"]["Window size"],
                          pos=Config["UI behavior"]["Output windows container"]["Window position"])                          
        self.InitializeMenuBar()
        self.messageProcessingGraphWindow = messageProcessingGraphWindow
        self._auiMgr = aui.AuiManager()
        self._auiMgr.SetManagedWindow(self)
        
        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MOVE, self.OnMove)
        
    def OnMove(self, event):
        Config["UI behavior"]["Output windows container"]["Window position"] = [self.GetPosition()[0], self.GetPosition()[1]]
        event.Skip()
                
    def OnSize(self, event):
        Config["UI behavior"]["Output windows container"]["Window size"] = [self.GetSize()[0], self.GetSize()[1]]
        event.Skip()

    def InitializeMenuBar(self):
        graphMenu = wx.Menu()
        self.Bind(wx.EVT_MENU, (lambda event: [self.messageProcessingGraphWindow.Show(), self.messageProcessingGraphWindow.Raise()]), graphMenu.Append(wx.NewId(), "Show message processing graph"))

        mb = wx.MenuBar()
        mb.Append(graphMenu, "Graph")
        self.SetMenuBar(mb)

    def AddNewSubWindow(self, subWindow, caption=None, pos=wx.LEFT):
        if len(self._auiMgr.GetAllPanes()) == 0:
            pos=wx.CENTER
        self._auiMgr.AddPane(subWindow, pos, caption)
        self._auiMgr.GetPaneByWidget(subWindow).DestroyOnClose(True)
        self._auiMgr.Update()
        if Config["UI behavior"]["Output windows container"]["Show after adding new window"]:
            self.Show()
        
    def OnClose(self, event):
        if self.messageProcessingGraphWindow.IsShown():
            self.Hide()
        else:
            ConfirmApplicationExit(self.messageProcessingGraphWindow, self)

    def Show(self, show=True):
        wx.Frame.Show(self, show)
        self.Raise()
