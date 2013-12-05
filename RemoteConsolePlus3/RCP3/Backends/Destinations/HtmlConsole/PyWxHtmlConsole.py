#Created by Dmytro Konobrytskyi, 2013 (github.com/Akson)
import wx.html
from wx.lib.agw import aui
from threading import Lock
from RCP3.OutputWindowsContainer import OutputWindowsContainer
import json
from RCP3.CommonUIRoutines import ShowDictAsList

class HTMLConsole(wx.Panel):
    '''
    This destination class is the default console window
    which does show messages as HTML
    '''

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        self._messagesList = []
        self._needUpdate = False
        self._lockedView = False
        
        self._htmlWindow = wx.html.HtmlWindow(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        '''
        tb = self.BuildToolbar()
        sizer.Add( tb, 0, wx.ALL | wx.ALIGN_LEFT | wx.EXPAND, 4 ) # add the toolbar to the sizer
        '''

        sizer.Add(self._htmlWindow, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_IDLE, self.CheckIfNeedUpdate)
        
        #Check every 50ms if there is a need to update the view due to recent messages
        self._mainTimer = wx.Timer(self, wx.ID_ANY)
        self._mainTimer.Start(50)
        self.Bind(wx.EVT_TIMER, self.CheckIfNeedUpdate, self._mainTimer)

        self._messagesListLock = Lock()
        self.SetSize((250, 200))
        
        self.Bind(wx.html.EVT_HTML_LINK_CLICKED, self.OnLinkClicked)
    
    def OnLinkClicked(self, evt):
        href = evt.GetLinkInfo().GetHref()
        if href.find("PyShowDict=") == 0:
            ShowDictAsList(json.loads(href[len("PyShowDict="):]))
        
    def BuildToolbar( self ) :
        tb = aui.AuiToolBar( self, -1 )
        self.ToolBar = tb
        tb.SetToolBitmapSize( ( 8, 8) )# this required for non-standard size buttons on MSW

        self.Bind(wx.EVT_TOOL, self.OnToolLock, source = tb.AddSimpleTool(wx.ID_ANY, 'Lock view', wx.Image(r'RCP2Console\Resources\Lock.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Lock current view while processing messagse'))
        self.Bind(wx.EVT_TOOL, self.OnToolSettings, source = tb.AddSimpleTool(wx.ID_ANY, 'Settings', wx.Image(r'RCP2Console\Resources\Configure.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Open settings window'))
        self.Bind(wx.EVT_TOOL, self.OnToolClear, source = tb.AddSimpleTool(wx.ID_ANY, 'Clear', wx.Image(r'RCP2Console\Resources\Clear.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(), 'Clear all HTML text from console'))
        
        tb.Realize()

        return tb
            
    def OnToolClear(self, event=None):
        self._messagesListLock.acquire()
        self._messagesList = []
        self._needUpdate = True
        self._messagesListLock.release()
            
    def OnToolLock(self, event=None):
        self._lockedView = not self._lockedView
            
    def OnToolSettings(self, event=None):
        print "OnToolSettings"
            
    def CheckIfNeedUpdate(self, event=None):
        if self._needUpdate:
            self.Refresh()
        
    def OnPaint(self, event=None):
        if self._needUpdate and not self._lockedView:
            self._messagesListLock.acquire()

            consoleText = '<body><font face="Consolas">'
            consoleText += "<br>".join(self._messagesList)
            consoleText += "</font></body>"
    
            self._needUpdate = False
            
            self._messagesListLock.release()
            
            #Update console content and scroll to the bottom
            self._htmlWindow.Freeze()
            self._htmlWindow.SetPage(consoleText)
            self._htmlWindow.Scroll(0, self._htmlWindow.GetScrollRange(wx.VERTICAL)) 
            self._htmlWindow.Thaw()
        
        dc = wx.PaintDC(self)#We need to create for solving infinity EVT_PAINT problem

    def AddHtmlLine(self, htmlLine):
        self._messagesListLock.acquire()
        #Save new message to buffer
        self._messagesList.append(htmlLine)
        #Limit buffer size
        self._messagesList = self._messagesList[-1000:]
        #Request redrawing
        self._needUpdate = True
        self._messagesListLock.release()

class Backend(object):
    def __init__(self, parentNode):
        self._parentNode = parentNode
        self._htmlConsole = None
        self.ShowWindow()

    def ShowWindow(self):
        if self._htmlConsole == None:
            self._htmlConsole = HTMLConsole(OutputWindowsContainer.Instance())
            OutputWindowsContainer.Instance().AddNewSubWindow(self._htmlConsole)
            self._htmlConsole.Bind(wx.EVT_WINDOW_DESTROY, self.OnDestroyOutputWindow)
        else:
            OutputWindowsContainer.Instance().Show()

    def OnDestroyOutputWindow(self, event):
        self._htmlConsole = None

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
        if self._htmlConsole:
            self._htmlConsole.AddHtmlLine(str(message["Data"]))

    def Delete(self):
        """
        This method is called when a parent node is deleted.
        """
        if self._htmlConsole:
            self._htmlConsole.Close()
