'''Created by Dmytro Konobrytskyi, 2012(C)'''
import wx
from wx.lib.agw import aui

class OutputWindowsContainer(wx.Frame):
    '''
    This is a main window that may have multiple subwindows managed by AuiManager
    '''
    def __init__(self):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title="RCP3 Console", size=(800, 600))
        self._auiMgr = aui.AuiManager()
        self._auiMgr.SetManagedWindow(self)
        
    def AddNewSubWindow(self, subWindow, caption=None, pos=wx.LEFT):
        if len(self._auiMgr.GetAllPanes()) == 0:
            pos=wx.CENTER
        self._auiMgr.AddPane(subWindow, pos, caption)
        self._auiMgr.GetPaneByWidget(subWindow).DestroyOnClose(True)
        self._auiMgr.Update()
        
    _instance = None
    @staticmethod
    def Instance():
        if OutputWindowsContainer._instance == None:
            OutputWindowsContainer._instance = OutputWindowsContainer()
        return OutputWindowsContainer._instance