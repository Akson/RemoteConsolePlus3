#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import wx
from RCP3.OutputWindowsContainer import OutputWindowsContainer
import cv2

class ImageViewer(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, 
                          None, 
                          id=wx.ID_ANY, 
                          title="RCP Image viewer")                          

        self.bmp = None
        self.width = 0
        self.height = 0

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_CLOSE, self.OnClose)

    def OnClose(self, event):
        self.Hide()

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        if self.bmp:
            dc.DrawBitmap(self.bmp, 0, 0)

    def SetImage(self, img):
        height, width = img.shape[:2]
        self.SetSize((width, height))
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
            self._imageViewer = ImageViewer()
            self._imageViewer.Show()
        else:
            self._imageViewer.Show()

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
