from ConfigUtils import *
from Const import *
import locale
import math

class DownloadFile:

	def __init__(self, fileURL):
		#self.conf = Config()
		self.fileURL = str(fileURL)
		self.accessUsername = ''
		self.accessPassword = ''
		self.percentage = 0
		self.formInfo = None
		self.formAction = None
		self.id = None
		self.numberOfPart = Config.settings.maxConnectionPerFile
		self.linkType = Config.getLinkType(self.fileURL)
		self.retry = 0
		if (self.linkType == RAPIDSHARE_FOLDER):
			self.fileName = FOLDER_TMP_NAME
		elif (self.linkType == URLCASH):
			self.fileName = URLCASH_TMP_NAME
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
			#print 'getFileName not none: ' , self.fileName, str(self.fileName)
			return str(self.fileName)
		else:
			#print 'getFileName NONE ' 
			return str(Config.getFileNameFromURL(self.getFileURL()))
	
	def getFileSize(self):
		return self.fileSize
		
	def getPartSize(self):
		return self.partSize
	
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
			#self.percentage = int(math.ceil((float(self.getByteDownloaded()) / self.getFileSize()) * 100))
			self.percentage = (float(self.getByteDownloaded()) / self.getFileSize()) * 100
		return self.percentage

	def getFormattedPercentage(self):
		return "%.1f%%" % self.getPercentage()

	def getFormattedSpeed(self):
		return "%.2f KB/s" % self.getSpeed()
		
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
	
	
	def getAccessPassword(self):
		return self.accessPassword	
	
	

	def setFileURL(self, fileURL):
		self.fileURL = fileURL
		
	def setFileName(self, fileName):
		#print 'setFileName ', fileName
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
	

	def setAccessPassword(self, password):
		self.accessPassword = password
		
		
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
		#print 'downloadFile ', self
		self.percentage = 0
		self.formInfo = None
		self.formAction = None		
		self.numberOfPart = Config.settings.maxConnectionPerFile
		self.retry = 0
		self.linkType = Config.getLinkType(self.fileURL)
		if (self.linkType == RAPIDSHARE_FOLDER):
			self.fileName = FOLDER_TMP_NAME
		elif (self.linkType == URLCASH):
			self.fileName = URLCASH_TMP_NAME
		else:
			self.fileName = None
		#print 'Reset fileName is ', self.fileName
		self.fileSize = 0
		self.fileType = ''
		self.byteDownloaded = 0
		self.status = STAT_Q
		self.downloadPartList = []
		self.errorStr = ''
		self.resumable = False


	def addDownloadPart(self, downloadPart):
		self.downloadPartList.append(downloadPart)
		
	def removeDownloadParts(self):
		self.downloadPartList = []		
		
	def getInfoByCol(self, colId):
		if (colId == FILEID_COL):
			return str(self.getId())
		elif (colId == FILENAME_COL):
			return str(self.getFileName())
		elif (colId == FILESTATUS_COL):
			return str(downloadStatus[self.getStatus()])
		elif (colId == FILESPEED_COL):
			#return str("%.2f" % self.getSpeed()) + ' KBps'
			return self.getFormattedSpeed()
		elif (colId == FILESIZE_COL):
			locale.setlocale(locale.LC_ALL, "")
			num = math.ceil(self.getFileSize() / 1024)		
			return str(locale.format("%d", num, True)) + ' KB'
		elif (colId == FILECOMP_COL):
			locale.setlocale(locale.LC_ALL, "")
			num = math.ceil(self.getByteDownloaded() / 1024)
			return str(locale.format("%d", num, True)) + ' KB'
		elif (colId == PERCENT_COL):
			#return str(self.getPercentage()) + ' %'
			return self.getFormattedPercentage()
		elif (colId == RETRY_COL):
			return str(self.getRetry())
		elif (colId == FILEURL_COL):
			return str(self.getFileURL())
		elif (colId == FILEERROR_COL):
			return str(self.getErrorStr())
		