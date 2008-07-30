import wx

class MainPanel(wx.Panel):
	def __init__(self, parent, id):
		wx.Panel.__init__(self, parent, id)	
		self.quote = wx.StaticText(self, -1, "Your quote :",wx.Point(0, 0))
		self.logger = wx.TextCtrl(self,5, "",wx.Point(300,20), wx.Size(200,300),wx.TE_MULTILINE)
		self.button =wx.Button(self, 10, "Save", wx.Point(200, 325))