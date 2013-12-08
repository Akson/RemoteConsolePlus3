#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import wx
from RCP3.OutputWindowsContainer import OutputWindowsContainer

class ImageViewer(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self.bmp = None
        self.width = 0
        self.height = 0

        self.Bind(wx.EVT_PAINT, self.OnPaint)

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        if self.bmp:
            dc.DrawBitmap(self.bmp, 0, 0)

    def SetImage(self, img):
        print img.shape
        height, width = img.shape[:2]
        if self.bmp == None or self.height != height or self.width != width:
            self.height = height
            self.width = width
            self.bmp = wx.BitmapFromBuffer(self.width, self.height, img)
            
        self.bmp.CopyFromBuffer(img)
        self.Refresh()

class Backend(object):
    def __init__(self, parentNode):
        self._parentNode = parentNode
        self._imageViewer = None
        self.ShowWindow()

    def ShowWindow(self):
        if self._imageViewer == None:
            self._imageViewer = ImageViewer(OutputWindowsContainer.Instance())
            OutputWindowsContainer.Instance().AddNewSubWindow(self._imageViewer)
            self._imageViewer.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroyOutputWindow)
        else:
            OutputWindowsContainer.Instance().Show()

    def OnDestroyOutputWindow(self, event):
        self._imageViewer = None

    def AppendContextMenuItems(self, menu):
        item = wx.MenuItem(menu, wx.NewId(), "Show output window")
        menu.Bind(wx.EVT_MENU, (lambda evt: self.ShowWindow()), item)
        menu.AppendItem(item)

    def GetParameters(self):
        """
        Returns a dictionary with object parameters, their values, 
        limits and ways to change them.
        """
        return {}
    
    def SetParameters(self, parameters):
        """
        Gets a dictionary with parameter values and
        update object parameters accordingly
        """
        pass
    
    def ProcessMessage(self, message):
        """
        This message is called when a new message comes. 
        If an incoming message should be processed by following nodes, the 
        'self._parentNode.SendMessage(message)'
        should be called with an appropriate message.
        """
        if self._imageViewer:
            self._imageViewer.SetImage(message["Data"])

    def Delete(self):
        """
        This method is called when a parent node is deleted.
        """
        if self._imageViewer:
            self._imageViewer.Close()
