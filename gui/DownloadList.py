import wx
import time
ID_COL = 0
FILENAME_COL = 1
FILESTATUS_COL = 2
FILESIZE_COL = 3
FILECOMP_COL = 4
PERCENT_COL = 5
FILEURL_COL = 6
class DownloadList(wx.ListCtrl):
	def __init__(self, parent, id, fileList = None):
		wx.ListCtrl.__init__(self, parent, id, style = wx.LC_REPORT | wx.LC_VIRTUAL)
		self.fileList = fileList
		self.InsertColumn(ID_COL, 'ID')
		self.InsertColumn(FILESTATUS_COL, 'Status')
		self.InsertColumn(FILENAME_COL, 'Filename')
		self.InsertColumn(FILESIZE_COL, 'File size')
		self.InsertColumn(FILECOMP_COL, 'Compeleted')
		self.InsertColumn(PERCENT_COL, 'Percentage')
		self.InsertColumn(FILEURL_COL, 'Address')
		#self.SetColumnWidth(ID_COL, 50)
		#self.SetColumnWidth(FILESTATUS_COL, wx.LIST_AUTOSIZE)
		#self.SetColumnWidth(FILENAME_COL, wx.LIST_AUTOSIZE)
		#self.SetColumnWidth(FILECOMP_COL, wx.LIST_AUTOSIZE)
		#self.SetColumnWidth(PERCENT_COL, wx.LIST_AUTOSIZE)
		#self.SetColumnWidth(FILEURL_COL, wx.LIST_AUTOSIZE)
		self.updateTime = time.time()
	
	def update(self, downloadingFile):
				
		if (downloadingFile.getListId() == None):
			print '----- New ITEM'
			index = self.InsertStringItem(downloadingFile.getId(), '')
			self.SetStringItem(index, ID_COL, str(downloadingFile.getId()))			
			self.SetStringItem(index, FILENAME_COL, str(downloadingFile.getFileName()))
			self.SetStringItem(index, FILESTATUS_COL, 'Downloading')
			self.SetStringItem(index, FILESIZE_COL, str(downloadingFile.getFileSize()))
			self.SetStringItem(index, FILECOMP_COL, str(downloadingFile.getCompleted()))
			self.SetStringItem(index, PERCENT_COL, str(downloadingFile.getPercentage()))
			self.SetStringItem(index, FILEURL_COL, str(downloadingFile.getURL()))		
			downloadingFile.setListId(index)
			self.Refresh()			
		else:
			#print '------ UPDATE ITEM: ', downloadingFile.getListId(), ' : ', downloadingFile.getCompleted()
			if (time.time() - self.updateTime > 0.5):
				print '------ UPDATE ITEM: ', downloadingFile.getListId(), ' : ', downloadingFile.getCompleted()
				self.updateTime = time.time()
				self.SetStringItem(downloadingFile.getListId(), PERCENT_COL, str(downloadingFile.getCompleted()))
				self.Refresh()