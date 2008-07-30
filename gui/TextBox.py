import wx
ID_BUTOK = 101
ID_BUTCLEAR = 102


class TextBox(wx.Frame):
	def __init__(self, parent, id, title, pos, size, callback):
		wx.Frame.__init__(self, parent, id, title, pos, size)
		self.callback = callback
		#self.panel = wx.Panel(self, wx.ID_ANY, pos, size, style = wx.STAY_ON_TOP)
		self.sizerVertical = wx.BoxSizer(wx.VERTICAL)
		self.textBox = wx.TextCtrl(self, wx.ID_ANY, style = wx.TE_MULTILINE)
		
		self.buttonOK = wx.Button(self, ID_BUTOK, 'OK')
		wx.EVT_BUTTON(self, ID_BUTOK, self.OnClickOk)
		self.buttonClear = wx.Button(self, ID_BUTCLEAR, 'Clear')
		wx.EVT_BUTTON(self, ID_BUTCLEAR, self.OnClickClear)
		
		self.sizerHorizontal = wx.BoxSizer(wx.HORIZONTAL)
		self.sizerHorizontal.Add(self.buttonOK, 1, wx.EXPAND)
		self.sizerHorizontal.Add(self.buttonClear, 1, wx.EXPAND)
		
		self.sizerVertical.Add(self.textBox, 1, wx.EXPAND)
		self.sizerVertical.Add(self.sizerHorizontal, 0, wx.ALIGN_CENTER)
		self.SetSizer(self.sizerVertical)
		
		self.SetAutoLayout(True)
		self.Center(wx.BOTH)		
		self.Show(True)
		
	def OnClickOk(self, event):
		if (self.textBox.GetValue().strip() != ''):
			self.callback(self.textBox.GetValue())
		self.Destroy()
		
	def OnClickClear(self, event):
		self.textBox.SetValue('')