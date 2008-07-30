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

	def removeFileFromDownloadList(self, removeDownloadFile, moveToCompleted = None):
		#print '----------------------------- removing ', removeDownloadFile
		i = 0
		self.downloadFileListLock.acquire()
		for downloadFile in self.downloadFileList:
			if (downloadFile.getFileURL() == removeDownloadFile.getFileURL()):
				if (moveToCompleted == None):
					del self.downloadFileList[i]
				else:
					downloadFile = self.downloadFileList.pop(i)
					self.completedFileList.append(downloadFile)
				break
			i += 1
		self.downloadFileListLock.release()
			
	def removeFileFromCompletedList(self, removeDownloadFile, moveToDownload = None):
		#print '----------------------------- removing ', removeDownloadFile
		i = 0
		self.completedFileListLock.acquire()
		for downloadFile in self.completedFileList:
			if (downloadFile.getFileURL() == removeDownloadFile.getFileURL()):
				if (moveToCompleted == None):
					del self.completedFileList[i]
				else:
					downloadFile = self.completedFileList.pop(i)
					self.downloadFileList.append(downloadFile)
				break
			i += 1
		self.completedFileListLock.release()
			
			
	def removeFileURLFromDownloadList(self, fileURL):
		i = 0
		self.downloadFileListLock.acquire()
		for downloadFile in self.downloadFileList:
			if (downloadFile.getFileURL() == fileURL):
				del self.downloadFileList[i]
				break
			i += 1
		self.downloadFileListLock.release()
			
	def removeFileURLFromCompletedList(self, fileURL):
		i = 0
		self.completedFileListLock.acquire()
		for downloadFile in self.completedFileList:
			if (downloadFile.getFileURL() == fileURL):
				del self.completedFileList[i] 
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
				
	def getDownloadFileByFileURL(self, fileURL):
		self.downloadFileListLock.acquire()
		for downloadFile in self.downloadFileList:
			if (downloadFile.getFileURL() == fileURL):
				self.downloadFileListLock.release()
				return downloadFile
		self.downloadFileListLock.release()
		
	def changeStatus(self, fileURL, status):
		self.getDownloadFileByFileURL(fileURL).setStatus(status)
		
		
	def emptyList(self):
		self.downloadFileListLock.acquire()
		self.downloadFileList = []
		self.downloadFileListLock.release()
		