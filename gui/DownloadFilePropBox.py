
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

		self.fileNameTextSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.fileNameText = wx.StaticText(self.panel, wx.ID_ANY, 'File name: ')
		self.fileNameTextValue = wx.StaticText(self.panel, wx.ID_ANY, str(self.downloadFile.getFileName()))		 
		self.fileNameTextSizer.Add(self.fileNameText, 0, wx.EXPAND)
		self.fileNameTextSizer.Add(self.fileNameTextValue, 0, wx.EXPAND)
		
		self.fileSizeTextSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.fileSizeText = wx.StaticText(self.panel, wx.ID_ANY, 'File size: ')
		self.fileSizeTextValue = wx.StaticText(self.panel, wx.ID_ANY, str(self.downloadFile.getFileSize()))
		self.fileSizeTextSizer.Add(self.fileSizeText, 0, wx.EXPAND)
		self.fileSizeTextSizer.Add(self.fileSizeTextValue, 0, wx.EXPAND)
		
		self.completedTextSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.completedText = wx.StaticText(self.panel, wx.ID_ANY, 'Completed: ')
		self.completedTextValue = wx.StaticText(self.panel, wx.ID_ANY, str(self.downloadFile.getByteDownloaded()))
		self.completedTextSizer.Add(self.completedText, 0, wx.EXPAND)
		self.completedTextSizer.Add(self.completedTextValue, 0, wx.EXPAND)

		self.retryTextSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.retryText = wx.StaticText(self.panel, wx.ID_ANY, 'Tried: ')
		self.retryTextValue = wx.StaticText(self.panel, wx.ID_ANY, str(self.downloadFile.getRetry()))
		self.retryTextSizer.Add(self.retryText, 0, wx.EXPAND)
		self.retryTextSizer.Add(self.retryTextValue, 0, wx.EXPAND)
		
		self.percentTextSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.percentText = wx.StaticText(self.panel, wx.ID_ANY, 'Percent: ')
		#self.percentTextValue = wx.StaticText(self.panel, wx.ID_ANY, str(self.downloadFile.getPercentage()))
		self.percentTextValue = wx.StaticText(self.panel, wx.ID_ANY, self.downloadFile.getFormattedPercentage())
		self.percentTextSizer.Add(self.percentText, 0, wx.EXPAND)
		self.percentTextSizer.Add(self.percentTextValue, 0, wx.EXPAND)

		self.statusTextSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.statusText = wx.StaticText(self.panel, wx.ID_ANY, 'Status: ')
		self.statusTextValue = wx.StaticText(self.panel, wx.ID_ANY, str(downloadStatus[self.downloadFile.getStatus()]))
		self.statusTextSizer.Add(self.statusText, 0, wx.EXPAND)
		self.statusTextSizer.Add(self.statusTextValue, 0, wx.EXPAND)

		self.numberOfPartTextSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.numberOfPartText = wx.StaticText(self.panel, wx.ID_ANY, 'Number of part: ')
		self.numberOfPartTextValue = wx.StaticText(self.panel, wx.ID_ANY, str(self.downloadFile.getNumberOfPart()))
		self.numberOfPartTextSizer.Add(self.numberOfPartText, 0, wx.EXPAND)
		self.numberOfPartTextSizer.Add(self.numberOfPartTextValue, 0, wx.EXPAND)		

		self.buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.okBut = wx.Button(self.panel, ID_OK_BUT, 'OK')
		wx.EVT_BUTTON(self, ID_OK_BUT, self.onClickOK)
		self.cancelBut = wx.Button(self.panel, ID_CANCEL_BUT, 'Cancel')
		wx.EVT_BUTTON(self, ID_CANCEL_BUT, self.onClickCancel)		
		self.buttonsSizer.Add(self.okBut, 1, wx.EXPAND)	
		self.buttonsSizer.Add(self.cancelBut, 1, wx.EXPAND)
		
		
		
		
		self.mainSizer.Add(self.urlSizer, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.fileNameTextSizer, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.fileSizeTextSizer, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.completedTextSizer, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.retryTextSizer, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.percentTextSizer, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.statusTextSizer, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.numberOfPartTextSizer, 0, wx.ALIGN_CENTER)
		self.mainSizer.Add(self.buttonsSizer, 0, wx.ALIGN_CENTER)
		
		self.panel.SetSizerAndFit(self.mainSizer)
		self.Center(wx.BOTH)
		#self.Fit()
		self.Show(True)
		
	def onClickOK(self, event):
		if (self.urlField.GetValue().strip() != self.downloadFile.getFileURL()):
			self.downloadFile.setFileURL(self.urlField.GetValue())
			if (self.downloadFile.getStatus() == STAT_D):
				self.parent.setSelectedIds([self.downloadFile.getId()])
				self.parent.onResetDownload(None)
			else:
				self.parent.update(self.downloadFile, [FILEURL_COL, FILESTATUS_COL, RETRY_COL])
		self.Destroy()
				
	def onClickCancel(self, event):
		self.Destroy()

	def getDownloadFileId(self):
		return self.downloadFile.getId()
		
	def setDownloadFile(self, downloadFile):
		self.downloadFile = downloadFile

	def updateInfo(self):
		self.fileNameTextValue.SetLabel(str(self.downloadFile.getFileName()))		 
		self.fileSizeTextValue.SetLabel(str(self.downloadFile.getFileSize()))
		self.completedTextValue.SetLabel(str(self.downloadFile.getByteDownloaded()))
		self.retryTextValue.SetLabel(str(self.downloadFile.getRetry()))
		#self.percentTextValue.SetLabel(str(self.downloadFile.getPercentage()))
		self.percentTextValue.SetLabel(self.downloadFile.getFormattedPercentage())
		self.statusTextValue.SetLabel(str(downloadStatus[self.downloadFile.getStatus()]))
		self.numberOfPartTextValue.SetLabel(str(self.downloadFile.getNumberOfPart()))
	
		