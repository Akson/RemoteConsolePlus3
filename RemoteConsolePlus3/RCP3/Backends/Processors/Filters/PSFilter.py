#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import wx

class ProcessingSuequenceAskingDialog(wx.Dialog):
    def __init__(self, currentProcessingSequenceName = ""):
        super(ProcessingSuequenceAskingDialog, self).__init__(parent=None, size=(270, 120)) 
        self._originalProcessingSequenceName = currentProcessingSequenceName
        self.allowedProcessingSequenceName = currentProcessingSequenceName
        
        self.InitUI()
        self.SetTitle("Configure filter")
        
    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox = wx.BoxSizer(wx.HORIZONTAL)        
        hbox.Add(wx.StaticText(self, label='Allowed processing sequence name:'), flag=wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.EXPAND, border=5)
        vbox.Add(hbox, flag=wx.ALL|wx.EXPAND, border=5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)        
        self.addressTextCtrl = wx.TextCtrl(self)
        self.addressTextCtrl.SetValue(self.allowedProcessingSequenceName)
        hbox.Add(self.addressTextCtrl, proportion=1, flag=wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.EXPAND, border=5)
        vbox.Add(hbox, flag=wx.ALL|wx.EXPAND, border=5)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox.Add(okButton)
        hbox.Add(closeButton, flag=wx.LEFT, border=5)
        vbox.Add(hbox, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=5)

        self.SetSizer(vbox)
        
        okButton.Bind(wx.EVT_BUTTON, self.SaveNewAddresAndClose)
        closeButton.Bind(wx.EVT_BUTTON, self.RestoreOriginalAndClose)
        self.Bind(wx.EVT_CLOSE, self.RestoreOriginalAndClose)
       
    def SaveNewAddresAndClose(self, e):
        self.allowedProcessingSequenceName = self.addressTextCtrl.GetValue()
        self.Destroy()

    def RestoreOriginalAndClose(self, e):
        self.allowedProcessingSequenceName = self._originalProcessingSequenceName
        self.Destroy()


class Backend(object):
    def __init__(self, parentNode):
        self._parentNode = parentNode
        self._allowedProcessingSequence = ""

    def Delete(self):
        """
        This method is called when a parent node is deleted.
        """
        pass
    
    def GetParameters(self):
        """
        Returns a dictionary with object parameters, their values, 
        limits and ways to change them.
        """
        return {"allowedProcessingSequence":self._allowedProcessingSequence}
    
    def SetParameters(self, parameters):
        """
        Gets a dictionary with parameter values and
        update object parameters accordingly
        """
        self._allowedProcessingSequence = parameters.get("allowedProcessingSequence", "")
        self.text = self._allowedProcessingSequence
    
    def ProcessMessage(self, message):
        """
        This message is called when a new message comes. 
        If an incoming message should be processed by following nodes, the 
        'self._parentNode.SendMessage(message)'
        should be called with an appropriate message.
        """
        if message["Info"].get("ProcessingSequence", None) == self._allowedProcessingSequence:
            self._parentNode.SendMessage(message)
        
    def AppendContextMenuItems(self, menu):
        """
        Append backend specific menu items to a context menu that user will see
        when he clicks on a node.
        """
        item = wx.MenuItem(menu, wx.NewId(), "Select allowed processing sequence")
        menu.Bind(wx.EVT_MENU, self.OnSelectAllowedProcessingSequence, item)
        menu.AppendItem(item)

    def OnSelectAllowedProcessingSequence(self, evt):
        dialog = ProcessingSuequenceAskingDialog(self._allowedProcessingSequence)
        dialog.ShowModal()
        dialog.Destroy()
        self.SetParameters({"allowedProcessingSequence":dialog.allowedProcessingSequenceName})
