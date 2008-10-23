import wx
ID_BUTOK = 101

class AddResultsBox(wx.Frame):
	def __init__(self, parent, id, text):
		wx.Frame.__init__(self, parent, id, 'Add url results')
		
		self.sizerVertical = wx.BoxSizer(wx.VERTICAL)
		self.textBox = wx.TextCtrl(self, wx.ID_ANY, style = wx.TE_MULTILINE | wx.TE_DONTWRAP | wx.TE_READONLY)
		self.textBox.SetValue(text)
		
		self.buttonOK = wx.Button(self, ID_BUTOK, 'OK')
		wx.EVT_BUTTON(self, ID_BUTOK, self.OnClickOk)
		
		self.sizerHorizontal = wx.BoxSizer(wx.HORIZONTAL)
		self.sizerHorizontal.Add(self.buttonOK, 1, wx.EXPAND)
	
		self.sizerVertical.Add(self.textBox, 1, wx.EXPAND)
		self.sizerVertical.Add(self.sizerHorizontal, 0, wx.ALIGN_CENTER)
		self.SetSizer(self.sizerVertical)
		
		self.SetAutoLayout(True)
		self.Center(wx.BOTH)		
		self.Show(True)

	def addResults(self, results):
		self.textBox.AppendText("\n" + results)		
		
	def OnClickOk(self, event):
		self.Destroy()