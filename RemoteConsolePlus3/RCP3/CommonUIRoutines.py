#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import wx
from RCP3.Configuration import Config
import sys

def ConfirmApplicationExit(messageProcessingGraphWindow, outputWindowsContainer):
    result = wx.ID_OK
    
    if Config["UI behavior"]["Ask before exit"] == True:
        dlg = wx.MessageDialog(None, "Do you really want to close this application and stop processing messages?", "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
    
    if result == wx.ID_OK:
        messageProcessingGraphWindow.Destroy()
        outputWindowsContainer.Destroy()






from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin, ColumnSorterMixin

actresses = [('jessica alba', 'pomona', '1981'), ('sigourney weaver', 'new york', '1949'),
    ('angelina jolie', 'los angeles', '1975'), ('natalie portman', 'jerusalem', '1981'),
    ('rachel weiss', 'london', '1971'), ('scarlett johansson', 'new york', '1984' )]


class PlainDictListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin, ColumnSorterMixin):
    def __init__(self, parent):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT)
        ListCtrlAutoWidthMixin.__init__(self)

class DictViewWindow(wx.Frame):
    def __init__(self, parent, windowId, title, size):
        wx.Frame.__init__(self, parent, windowId, title, size=size)

        hbox = wx.BoxSizer(wx.HORIZONTAL)

        panel = wx.Panel(self, -1)

        self.list = PlainDictListCtrl(panel)
        self.list.InsertColumn(0, 'Name', width=140)
        self.list.InsertColumn(1, 'Value', wx.LIST_FORMAT_LEFT, 90)

        for i in actresses:
            index = self.list.InsertStringItem(sys.maxint, i[0])
            self.list.SetStringItem(index, 1, i[1])

        hbox.Add(self.list, 1, wx.EXPAND)
        panel.SetSizer(hbox)

        self.Centre()
        self.Show(True)
        
        self.Bind(wx.EVT_CLOSE, (lambda e: self.Hide()))
        
    def SetDict(self, dictObj):
        self.dictObj = dictObj
        outputList = []
        self.ConvertDictToPropertiesListRecursively(dictObj, [], outputList)
        
        self.list.DeleteAllItems()
        for i in outputList:
            index = self.list.InsertStringItem(sys.maxint, str(i[0]))
            self.list.SetStringItem(index, 1, str(i[1]))
        
    def ConvertDictToPropertiesListRecursively(self, curDict, keysStack, outputList):
        print keysStack
        for key in curDict:
            if type(curDict[key]) != dict:
                outputList.append((".".join(keysStack+[key]), curDict[key]))

        for key in curDict:
            if type(curDict[key]) == dict:
                self.ConvertDictToPropertiesListRecursively(curDict[key], keysStack+[key], outputList)

class MessageInfoWindowInstance(object):
    messageInfoWindow = None
    
def ShowDictAsList(dictObj):
    print dictObj
    if MessageInfoWindowInstance.messageInfoWindow == None:
        MessageInfoWindowInstance.messageInfoWindow = DictViewWindow(None, -1, 'Message info', (380, 230))
        
    MessageInfoWindowInstance.messageInfoWindow.SetDict(dictObj)
    MessageInfoWindowInstance.messageInfoWindow.Show()
    MessageInfoWindowInstance.messageInfoWindow.Raise()