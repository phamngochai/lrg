import wx
from DownloadFileGrid import DownloadFileGrid
from Const import *

class PanelBot(wx.Panel):
	def __init__(self, parent, id, popupMenuCallback = None):
		wx.Panel.__init__(self, parent, id)
		#self.fileList = fileList
		self.SetBackgroundColour(wx.WHITE)
		self.downloadFileGrid = DownloadFileGrid(self, wx.ID_ANY, PANEL_BOT, popupMenuCallback)
		self.sizer = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer.Add(self.downloadFileGrid, 1, wx.EXPAND)
		self.SetSizer(self.sizer)	
		self.SetAutoLayout(True)
		
	def update(self, downloadFile, updateType):
		#pass
		self.downloadFileGrid.update(downloadFile, updateType)
		
	def addDownloadFile(self, downloadFile):
		self.downloadFileGrid.addDownloadFile(downloadFile)
		
	def deleteDownloadFile(self, downloadFile):
		self.downloadFileGrid.removeDownloadFile(downloadFile)
		
	def deleteDownloadFileURL(self, fileURL):
		self.downloadFileGrid.removeDownloadFileURL(fileURL)		
		
	def deleteAllDownloadFile(self):
		self.downloadFileGrid.removeAllDownloadFile()