
import wx
from Const import *

ID_OK_BUT = 90001
ID_CANCEL_BUT = 90002

class DownloadFilePropBox(wx.Frame):
	def __init__(self, parent, id, title, downloadFile):
		wx.Frame.__init__(self, parent, id, title, size = (350, 200))
		self.parent = parent
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

		tmpPercentText = 'Percent: ' + str(self.downloadFile.getPercentage())
		self.percentText = wx.StaticText(self.panel, wx.ID_ANY, tmpPercentText)

		tmpStatusText = 'Status: ' + str(downloadStatus[self.downloadFile.getStatus()])
		self.statusText = wx.StaticText(self.panel, wx.ID_ANY, tmpStatusText)
		

		self.buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.okBut = wx.Button(self.panel, ID_OK_BUT, 'OK')
		wx.EVT_BUTTON(self, ID_OK_BUT, self.onClickOK)
		self.cancelBut = wx.Button(self.panel, ID_CANCEL_BUT, 'Cancel')
		wx.EVT_BUTTON(self, ID_CANCEL_BUT, self.onClickCancel)		
		self.buttonsSizer.Add(self.okBut, 1, wx.EXPAND)	
		self.buttonsSizer.Add(self.cancelBut, 1, wx.EXPAND)
		
		
		
		
		self.mainSizer.Add(self.urlSizer, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.fileNameText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.fileSizeText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.completedText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.retryText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.percentText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.statusText, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.buttonsSizer, 0, wx.ALIGN_CENTER)
		
		self.panel.SetSizerAndFit(self.mainSizer)
		self.Center(wx.BOTH)
		#self.Fit()
		self.Show(True)
		
	def onClickOK(self, event):
		self.downloadFile.setFileURL(self.urlField.GetValue())
		self.parent.update(self.downloadFile, [FILEURL_COL, FILESTATUS_COL, RETRY_COL])
		self.Destroy()
				
	def onClickCancel(self, event):
		self.Destroy()
