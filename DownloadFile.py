from ConfigUtils import *
from Const import *


class DownloadFile:

	def __init__(self, fileURL):
		#self.conf = Config()
		self.fileURL = str(fileURL)
		#self.fileName = fileName
		#self.completed = completed
		self.percentage = 0
		self.formInfo = None
		self.formAction = None
		self.id = None
		self.numberOfPart = Config.settings.maxConnectionPerFile
		self.linkType = Config.getLinkType(self.fileURL)
		self.retry = 0
		if (self.linkType == RAPIDSHARE_FOLDER):
			self.fileName = FOLDER_TMP_NAME
		else:
			self.fileName = None
		self.fileSize = 0
		self.fileType = ''
		self.byteDownloaded = 0
		self.status = STAT_Q
		self.downloadPartList = []
		self.errorStr = ''
		self.resumable = False
				
	
	def getId(self):
		return self.id
		
	def getFileURL(self):
		return str(self.fileURL)
		
	def getFileType(self):
		return self.fileType
				
	def getFileName(self):
		if (self.fileName != None):
			return str(self.fileName)
		else:
			return str(Config.getFileNameFromURL(self.getFileURL()))
	
	def getFileSize(self):
		return self.fileSize
		
	def getPartSize(self):
		return self.partSize
		
	def getPercentage(self):
		return self.percentage
		
	def getByteDownloaded(self):
		return self.byteDownloaded
	
	def getStatus(self):
		return self.status
		
	def getFormInfo(self):
		return self.formInfo
	
	def getFormAction(self):	
		return self.formAction
		
	def getNumberOfPart(self):
		if (self.getResumable() == True):
			return self.numberOfPart
		else:
			return 1
		
	def getRetry(self):
		return self.retry
			
	def getPercentage(self):
		if (self.fileSize != 0):
			self.percentage = int(self.byteDownloaded / self.fileSize * 100)			
		return self.percentage
		
	def getByteDownloaded(self):
		byteDownloaded = 0
		for downloadPart in self.downloadPartList:
			byteDownloaded += downloadPart.getByteDownloaded()
		return byteDownloaded		
	
	def getSpeed(self):
		speed = 0
		for downloadPart in self.downloadPartList:
			speed += downloadPart.getSpeed()
		return speed
		
	def getDownloadPartList(self):
		return self.downloadPartList
		
	
	def getErrorStr(self):
		return self.errorStr
		
		
	def getResumable(self):
		return self.resumable
		
		
	def getDestinationFileName(self):
		#print 'self.getFileName() ', self.getFileName()
		return os.path.join(Config.settings.downloadDir, self.getFileName())
		
	
	def getLinkType(self):
		return self.linkType
	
	

	def setFileURL(self, fileURL):
		self.fileURL = fileURL
		
	def setFileName(self, fileName):
		if (self.linkType != RAPIDSHARE_FOLDER):
			self.fileName = fileName
		
	def setFileSize(self, fileSize):
		self.fileSize = fileSize
	
	def setFileType(self, fileType):
		self.fileType = fileType
		
	def setStatus(self, status):
		self.status = status
		
	def setCompleted(self, completed):		
		self.completed = completed
		
	def setErrorStr(self, errorStr):
		self.errorStr = errorStr		
		
	def setFormInfo(self, formInfo):
		self.formInfo = formInfo
	
	def setFormAction(self, formAction):
		self.formAction = formAction		
	
	def setId(self, id):
		self.id = id
				
	def setPartSize(self, partSize = None):
		if (partSize != None):
			self.partSize = partSize
		else:
			self.partSize = Config.getPartSize(self.getFileSize(), self.getNumberOfPart(), 0)
		
	def setResumable(self, resumable):
		self.resumable = resumable
	
		
	def isRetryPossible(self):
		if (self.retry + 1 > Config.settings.maxRetry):
			return False
		else:
			return True
	
	def increaseRetry(self):
		self.retry += 1
		
	def resetRetry(self):
		self.retry = 0
		
	def resetInfo(self):
		self.percentage = 0
		self.formInfo = None
		self.formAction = None		
		self.numberOfPart = Config.settings.maxConnectionPerFile
		self.retry = 0
		if (self.linkType == RAPIDSHARE_FOLDER):
			self.fileName = FOLDER_TMP_NAME
		else:
			self.fileName = None
		self.fileSize = 0
		self.fileType = ''
		self.byteDownloaded = 0
		self.status = STAT_Q
		self.downloadPartList = []
		self.errorStr = ''
		self.resumable = False

	def addDownloadPart(self, downloadPart):
		self.downloadPartList.append(downloadPart)
		
		
	def getInfoByCol(self, colId):
		if (colId == ID_COL):
			return str(self.getId())
		elif (colId == FILENAME_COL):
			return str(self.getFileName())
		elif (colId == FILESTATUS_COL):
			return str(downloadStatus[self.getStatus()])
		elif (colId == FILESPEED_COL):
			return str("%.2f" % self.getSpeed())
		elif (colId == FILESIZE_COL):
			return str(self.getFileSize())
		elif (colId == FILECOMP_COL):
			return str(self.getByteDownloaded())
		elif (colId == PERCENT_COL):
			return str(self.getPercentage())
		elif (colId == RETRY_COL):
			return str(self.getRetry())
		elif (colId == FILEURL_COL):
			return str(self.getFileURL())
		elif (colId == FILEERROR_COL):
			return str(self.getErrorStr())
		