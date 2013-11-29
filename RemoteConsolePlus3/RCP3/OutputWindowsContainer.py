'''Created by Dmytro Konobrytskyi, 2012(C)'''
import wx
from wx.lib.agw import aui
from RCP3.CommonUIRoutines import ConfirmApplicationExit

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
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title="RemoteConsole+", size=(800, 600))
        self.messageProcessingGraphWindow = messageProcessingGraphWindow
        self._auiMgr = aui.AuiManager()
        self._auiMgr.SetManagedWindow(self)
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        
    def AddNewSubWindow(self, subWindow, caption=None, pos=wx.LEFT):
        if len(self._auiMgr.GetAllPanes()) == 0:
            pos=wx.CENTER
        self._auiMgr.AddPane(subWindow, pos, caption)
        self._auiMgr.GetPaneByWidget(subWindow).DestroyOnClose(True)
        self._auiMgr.Update()
        self.Show()
        
    def OnClose(self, event):
        if self.messageProcessingGraphWindow.IsShown():
            self.Hide()
        else:
            ConfirmApplicationExit(self.messageProcessingGraphWindow, self)