#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import wx
from RCP3.Backends.Sources.ZMQ.Tools.RoutersListProvider import GetAvailableRoutersList

class ServerSelectionDialog(wx.Dialog):
    def __init__(self, currentServerAddress = None):
        super(ServerSelectionDialog, self).__init__(parent=None, size=(270, 260)) 
        self._originalServerAddress = currentServerAddress
        self.serverAddress = currentServerAddress
        
        self.availableServersList = GetAvailableRoutersList()
        self.currentlySelectedIdx = -1
        
        self.InitUI()
        self.SetTitle("Select router address")
        
    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)        
        hbox.Add(wx.StaticText(self, label='Router address:'), flag=wx.ALIGN_CENTER_VERTICAL)
        self.addressTextCtrl = wx.TextCtrl(self)
        self.addressTextCtrl.SetValue(self.serverAddress if self.serverAddress else "")
        hbox.Add(self.addressTextCtrl, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.EXPAND, border=5)
        vbox.Add(hbox, flag=wx.ALL|wx.EXPAND, border=5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.listBox = wx.ListBox(self, wx.NewId(), wx.DefaultPosition, (-1, 150), self.availableServersList, wx.LB_SINGLE)
        hbox.Add(self.listBox, proportion=1, flag=wx.EXPAND)
        vbox.Add(hbox, flag=wx.ALL|wx.EXPAND, border=5)
       
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        refreshButton = wx.Button(self, label='Refresh list')
        hbox.Add(okButton)
        hbox.Add(closeButton, flag=wx.LEFT, border=5)
        hbox.Add(refreshButton, flag=wx.LEFT, border=10)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=5)

        self.SetSizer(vbox)
        
        okButton.Bind(wx.EVT_BUTTON, self.SaveNewAddresAndClose)
        closeButton.Bind(wx.EVT_BUTTON, self.RestoreOriginalAndClose)
        refreshButton.Bind(wx.EVT_BUTTON, self.RefreshRoutersList)
        self.Bind(wx.EVT_CLOSE, self.RestoreOriginalAndClose)
        self.listBox.Bind(wx.EVT_LISTBOX, self.OnSelect)
        self.addressTextCtrl.Bind(wx.EVT_TEXT, self.OnText)
       
    def OnText(self, event):
        if self.availableServersList[self.currentlySelectedIdx] != self.addressTextCtrl.GetValue():
            self.currentlySelectedIdx = -1
            self.listBox.Select(self.currentlySelectedIdx)
        
    def OnSelect(self, event):
        self.currentlySelectedIdx = event.GetSelection()
        self.addressTextCtrl.SetValue(self.availableServersList[event.GetSelection()])
        self.listBox.Select(self.currentlySelectedIdx)

    def RefreshRoutersList(self, e=None):
        self.availableServersList = GetAvailableRoutersList()
        self.listBox.Set(self.availableServersList)
        self.listBox.Select(self.currentlySelectedIdx)
        
    def SaveNewAddresAndClose(self, e):
        self.serverAddress = self.addressTextCtrl.GetValue()
        self.Destroy()

    def RestoreOriginalAndClose(self, e):
        self.serverAddress = self._originalServerAddress
        self.Destroy()
