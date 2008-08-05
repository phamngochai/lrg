
import wx
from Const import *

class DownloadFilePropBox(wx.Frame):
	def __init__(self, parent, id, title, downloadFile):
		wx.Frame.__init__(self, parent, id, title, size = (300, 200))
		self.downloadFile = downloadFile
		self.panel = wx.Panel(self)
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)	
		
		self.urlSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.urlText = wx.StaticText(self.panel, wx.ID_ANY, 'URL: ')
		self.urlField = wx.TextCtrl(self.panel, wx.ID_ANY)
		self.urlField.SetValue(self.downloadFile.getFileURL())		
		self.urlSizer.Add(self.urlText, 1, wx.EXPAND)	
		self.urlSizer.Add(self.urlField, 10, wx.EXPAND)


		tmpFileNameText = 'File name: ' + str(self.downloadFile.getFileName())
		self.fileNameText = wx.StaticText(self.panel, wx.ID_ANY, tmpFileNameText)

		tmpFileSizeText = 'File size: ' + str(self.downloadFile.getFileSize())
		self.fileSizeText = wx.StaticText(self.panel, wx.ID_ANY, tmpFileSizeText)

		tmpCompletedText = 'Completed: ' + str(self.downloadFile.getByteDownloaded())
		self.completedText = wx.StaticText(self.panel, wx.ID_ANY, tmpCompletedText)


		tmpRetryText = 'Retry: ' + str(self.downloadFile.getRetry())
		self.retryText = wx.StaticText(self.panel, wx.ID_ANY, tmpRetryText)
		
		self.mainSizer.Add(self.urlSizer, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.fileNameText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.fileSizeText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.completedText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.retryText, 0, wx.ALIGN_CENTER)
		
		self.panel.SetSizerAndFit(self.mainSizer)
		self.Center(wx.BOTH)
		self.Fit()
		self.Show(True)
