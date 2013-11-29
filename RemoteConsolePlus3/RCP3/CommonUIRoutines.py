#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import wx

def ConfirmApplicationExit(messageProcessingGraphWindow, outputWindowsContainer):
    dlg = wx.MessageDialog(None, "Do you really want to close this application and stop processing messages?", "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
    result = dlg.ShowModal()
    dlg.Destroy()
    if result == wx.ID_OK:
        messageProcessingGraphWindow.Destroy()
        outputWindowsContainer.Destroy()
