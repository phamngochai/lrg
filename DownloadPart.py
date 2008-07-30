from ConfigUtils import *
from DownloadFile import DownloadFile
import os

class DownloadPart(DownloadFile):

	def __init__(self, downloadFile, partNo):
	
		#self.conf = Config()	
		self.partNo = partNo
		self.byteDownloaded = 0
		
		self.fileName = downloadFile.getFileName()
		self.fileSize = downloadFile.getFileSize()
		self.formInfo = downloadFile.getFormInfo()
		self.formAction = downloadFile.getFormAction()
		self.fileURL = downloadFile.getFileURL()
		self.numberOfPart = downloadFile.getNumberOfPart()
		self.resumable = downloadFile.getResumable()
		self.partSize = Config.getPartSize(self.fileSize, self.numberOfPart, 0)
		self.id = downloadFile.getId()
		
		self.tmpFileName = Config.getTmpFile(self.fileName, self.partNo)

		self.downloadRange = None
		self.size = 0
		self.retry = 0
		self.byteSaved = 0
		self.speed = 0
		self.completed = False
		self.seekPos = 0
		self.resuming = False
		
	
	#def getRetry(self):
		#return self.retry
	
	def getDownloadRange(self):
		return self.downloadRange
				
	def getByteDownloaded(self):
		return self.byteDownloaded + self.byteSaved
		
	def getTmpFileName(self):
		return str(self.tmpFileName)
		
	def getPartNo(self):
		return self.partNo
	
	def getSpeed(self):
		return self.speed

	def getFileSeekPos(self):
		return self.seekPos	

	def getDesinationFile(self):
		return os.path.join(Config.settings.tmpDir, self.getTmpFileName())

		
		

	def setTmpFileName(self, tmpFileName):
		self.tmpFileName = tmpFileName		
		
	def setDownloadRange(self, downloadRange):
		self.downloadRange = downloadRange
		
	#def setPartSize(self, partSize):
		#self.partSize = partSize
		
	#def setTotalByteDownloaded(self, byteDownloaded):
		#self.byteDownloaded = byteDownloaded


	#def setCompleted(self, completed):
		#self.completed = completed

	def setByteSaved(self, byteSaved):
		self.byteSaved = byteSaved
		
	def setSpeed(self, speed):
		self.speed = speed
		
	def setFileSeekPos(self, seekPos):
		self.seekPos = seekPos
		
	def setResuming(self, resuming):
		self.resuming = resuming
		
	def addByteDownloaded(self, byteDownloaded):
		self.byteDownloaded += byteDownloaded
	
	
	
	
	def resetByteDownloaded(self):
		self.byteDownloaded = 0
			
	def isCompleted(self):
		#return self.completed
		realPartSize = Config.getPartSize(self.getFileSize(), self.getNumberOfPart(), self.getPartNo())
		if (self.getByteDownloaded() == realPartSize):
			#print 'self.getByteDownloaded() ', self.getByteDownloaded(), ' ', self.getTmpFileName()
			#print 'self.getPartSize() ', self.getPartSize(), ' ', self.getTmpFileName()
			#print 'isCompleted() is True ', self.getTmpFileName()
			return True
		else:
			#print 'isCompleted() is False ', self.getTmpFileName(), ' saved ' ,self.getByteDownloaded(), ' actual ', realPartSize 
			return False
			
		
	def isRetryPossible(self):
		if (self.retry + 1 > Config.settings.maxRetry):
			return False
		else:
			return True
	def isResuming(self):
		return self.resuming	
	
	
	def increaseRetry(self):
		self.retry += 1
		
	#def addByteDownloaded(self, numberOfByte):
		#self.byteDownloaded = numberOfByte
		
		
	def setRange(self):	
	
		self.byteDownloaded = 0
		
		tmpFileName = self.getTmpFileName()
		partNo = self.getPartNo()
		partSize = self.getPartSize()
		fileSize = self.getFileSize()
		#print 'DownloadPart partNo', partNo
		#print 'DownloadPart partSize', partSize
		#print 'DownloadPart fileSize', fileSize
		
		if (Config.checkExistence(tmpFileName, 'F') >= 0 ):
			print 'DownloadPart, tmp file does exist'
			self.setResuming(True)
			
			currentSize = os.path.getsize(tmpFileName)			
			numberOfPart = self.getNumberOfPart()
			#fileSize = downloadPart.getFileSize()
			
			realPartSize = Config.getPartSize(fileSize, self.getNumberOfPart(), partNo)
			
			if (currentSize > realPartSize):
				print 'setRange BIGGER FILESIZE found, will be overwriten now ', self.getId()
				currentSize = 0
			
			resumeSize = Config.settings.resumeSize
			seekPos = currentSize - resumeSize
			if (seekPos < 0):
				seekPos = 0
			
			self.setFileSeekPos(seekPos)
			self.setByteSaved(seekPos)

			if (currentSize > resumeSize):
				beginPos = int(partNo * partSize) + currentSize - resumeSize
			else:
				beginPos = int(partNo * partSize)
						
			endPos = int((partNo + 1) * partSize - 1)
			
			if (endPos >= fileSize):
				endPos = fileSize - 1
				
			downloadRange = str(beginPos) + '-' + str(endPos)
			
		else:
			self.setResuming(False)
			print 'DownloadPart, tmp file does not exist'
			beginPos = int(partNo * partSize)
			endPos = int((partNo + 1) * partSize - 1)
			if (endPos >= fileSize):
				endPos = fileSize - 1
			downloadRange = str(beginPos) + '-' + str(endPos)
			
		#print 'DownloadPart downloadRange', downloadRange
			
		self.setDownloadRange(downloadRange)		
		
		
		