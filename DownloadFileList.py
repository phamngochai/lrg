from Const import *
from DownloadFile import DownloadFile
from threading import Lock

class DownloadFileList:

	def __init__(self):
		self.downloadFileList = []
		self.completedFileList = []
		self.downloadFileListLock = None
		self.completedFileListLock = None
				
	def setLock(self):
		self.downloadFileListLock = Lock()
		self.completedFileListLock = Lock()

	def unsetLock(self):
		self.downloadFileListLock.acquire()
		for downloadFile in self.downloadFileList:
			downloadFile.removeDownloadParts()
		self.downloadFileListLock.release()
		self.completedFileListLock.acquire()
		for downloadFile in self.completedFileList:
			downloadFile.removeDownloadParts()
		self.completedFileListLock.release()		
		self.downloadFileListLock = None
		self.completedFileListLock = None
		

		
	def getList(self, getCompletedList = None):
		if (getCompletedList == None):
			return self.downloadFileList
		else:
			return self.completedFileList
			
	def addQueueingFile(self, downloadFile):
		self.downloadFileListLock.acquire()
		self.downloadFileList.append(downloadFile)
		self.downloadFileListLock.release()

	def getQueueingFile(self):
		#print ' size of self.downloadFileList is ', len (self.downloadFileList)
		self.downloadFileListLock.acquire()
		for downloadFile in self.downloadFileList:
			#if (downloadFile.getStatus() == STAT_Q or (downloadFile.getStatus() == STAT_E and downloadFile.isRetryPossible())):
			#print 'Checking ', downloadFile.getFileURL(), ' status ', downloadFile.getStatus(), ' retryposible ', downloadFile.isRetryPossible()
			if (downloadFile.getStatus() == STAT_Q and downloadFile.isRetryPossible()):
				self.downloadFileListLock.release()
				return downloadFile
		#print 'NO Queueing file retriable found, return NONE'
		self.downloadFileListLock.release()
		return None


	def deleteDownloadFileFromDownloadList(self, id, moveToCompleted = None):			
		i = 0
		self.downloadFileListLock.acquire()
		for downloadFile in self.downloadFileList:
			if (downloadFile.getId() == id):
				if (moveToCompleted == None):
					del self.downloadFileList[i]
				else:
					downloadFile = self.downloadFileList.pop(i)
					self.completedFileListLock.acquire()
					self.completedFileList.append(downloadFile)
					self.completedFileListLock.release()
				break
			i += 1
		self.downloadFileListLock.release()	
		
		
			
	def deleteDownloadFileFromCompletedList(self, id, moveToDownload = None):
		i = 0
		self.completedFileListLock.acquire()
		for downloadFile in self.completedFileList:
			if (downloadFile.getId() == id):
				if (moveToDownload == None):
					del self.completedFileList[i]
				else:
					downloadFile = self.completedFileList.pop(i)
					self.downloadFileListLock.acquire()
					self.downloadFileList.append(downloadFile)
					self.downloadFileListLock.release()
				break
			i += 1
		self.completedFileListLock.release()
		
			

			
	def getNumberOfDownloadingFile(self):
		i = 0
		self.downloadFileListLock.acquire()
		for downloadFile in self.downloadFileList:
			if (downloadFile.getStatus() == STAT_D):
				i += 1
		self.downloadFileListLock.release()
		return i
		

	def getNumberOfQueueingFile(self):
		i = 0
		self.downloadFileListLock.acquire()
		for downloadFile in self.downloadFileList:
			if (downloadFile.getStatus() == STAT_Q and downloadFile.isRetryPossible()):
				i += 1
		self.downloadFileListLock.release()
		return i


	def resetStatus(self, status):
		self.downloadFileListLock.acquire()
		for downloadFile in self.downloadFileList:			
			if (downloadFile.getStatus() != STAT_D):
				#print 'Reseting', downloadFile.getFileURL(), ' to ', status
				downloadFile.setStatus(status)
				downloadFile.setErrorStr('')
		self.downloadFileListLock.release()
				
				
	def getDownloadFileById(self, id):
		self.downloadFileListLock.acquire()
		for downloadFile in self.downloadFileList:
			if (downloadFile.getId() == id):
				self.downloadFileListLock.release()
				return downloadFile
		self.downloadFileListLock.release()
		
		
	def changeStatus(self, id, status):
		self.getDownloadFileById(id).setStatus(status)
		
		
	def emptyList(self):
		self.downloadFileListLock.acquire()
		self.downloadFileList = []
		self.downloadFileListLock.release()
		