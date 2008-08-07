import wx
from DownloadFileGrid import DownloadFileGrid
from Const import *

class PanelTop(wx.Panel):
	def __init__(self, parent, id, popupMenuCallback = None):
		wx.Panel.__init__(self, parent, id)
		#self.parent = parent		
		self.SetBackgroundColour(wx.WHITE)
		self.downloadFileGrid = DownloadFileGrid(self, wx.ID_ANY, PANEL_TOP, popupMenuCallback)
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.downloadFileGrid, 1, wx.EXPAND)
		self.SetSizer(self.sizer)	
		self.SetAutoLayout(True)
		
	def update(self, downloadFile, updateType):
		#pass
		self.downloadFileGrid.update(downloadFile, updateType)
		
	def addDownloadFile(self, downloadFile):
		self.downloadFileGrid.addDownloadFile(downloadFile)
		
	def deleteDownloadFile(self, id):
		self.downloadFileGrid.deleteDownloadFile(id)
		
	def deleteAllDownloadFile(self):
		self.downloadFileGrid.removeAllDownloadFile()