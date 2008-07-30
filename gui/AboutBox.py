import wx
from Const import *

class AboutBox(wx.Frame):
	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, size = (300, 200))
		self.panel = wx.Panel(self)
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)		
		img = wx.Image(LOGOFILE, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
		#self.img = wx.StaticBitmap(self, -1, img, (10 + img.GetWidth(), 5), (img.GetWidth(), img.GetHeight()))
		self.img = wx.StaticBitmap(self.panel, -1, img)
		
		self.titleFont = wx.Font(12, wx.MODERN, wx.NORMAL, wx.FONTWEIGHT_BOLD)
		self.titleText = wx.StaticText(self.panel, wx.ID_ANY, 'Linux Rapidshare Grabber')
		self.titleText.SetFont(self.titleFont)
		self.versionText = wx.StaticText(self.panel, wx.ID_ANY, VERSION)
		self.licenseText = wx.StaticText(self.panel, wx.ID_ANY, 'LRG is licensed under GPL')
		self.gplURLText = wx.StaticText(self.panel, wx.ID_ANY, 'http://www.gnu.org/licenses/gpl.html')
		self.siteText = wx.StaticText(self.panel, wx.ID_ANY, 'LRG website: http://lrg.sourceforge.net')
		self.aboutText = wx.StaticText(self.panel, wx.ID_ANY, 'Created by PHAM Ngoc Hai')
		self.emailText = wx.StaticText(self.panel, wx.ID_ANY, 'Email: pngochai@yahoo.com')
		self.mysiteText = wx.StaticText(self.panel, wx.ID_ANY, 'http://www.phamngochai.net')
		self.lnhnText = wx.StaticText(self.panel, wx.ID_ANY, 'LN - HN')
		
		self.mainSizer.Add(self.img, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.titleText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.versionText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.licenseText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.gplURLText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.siteText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.aboutText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.emailText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.mysiteText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.lnhnText, 0, wx.ALIGN_CENTER)

		self.panel.SetSizerAndFit(self.mainSizer)
		self.Center(wx.BOTH)
		self.Fit()
		self.Show(True)
