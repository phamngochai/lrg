import wx

class TrayIcon(wx.TaskBarIcon):
	def __init__(self, icon, tooltip, frame):
		wx.TaskBarIcon.__init__(self)
		self.SetIcon(icon, tooltip)
		self.frame = frame
		self.Bind(wx.EVT_MENU, self.onShow,  id=1)
		self.Bind(wx.EVT_MENU, self.onClose, id=wx.ID_EXIT)
		self.Bind(wx.EVT_TASKBAR_LEFT_DCLICK, self.onShow)
	
	def onShow(self, e):
		if self.frame.IsIconized():
			self.frame.Iconize(False)
		if not self.frame.IsShown():
			self.frame.Show()
		self.frame.Raise()
	
	def onClose(self, e):
		self.frame.Close()
	
	def CreatePopupMenu(self):
		menu = wx.Menu()
		menu.Append(1, 'Show')
		menu.Append(wx.ID_EXIT, 'Exit')
		return menu
