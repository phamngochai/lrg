import os
import sys
import commands
import cPickle
from Const import *
from Settings import Settings
from math import *
import threading

class Config:

	def load():
						
		if (Config.checkExistence(CONFIG_DIR, TYPE_DIR) >= EXIST):
			pass
		else:
			os.mkdir(CONFIG_DIR)
		if (Config.checkExistence(DOWNLOAD_DIR, TYPE_DIR) >= EXIST):
			pass
		else:			
			os.mkdir(DOWNLOAD_DIR)
		if (Config.checkExistence(TMP_DIR, TYPE_DIR) >= EXIST):
			pass
		else:		
			os.mkdir(TMP_DIR)
			
		if (Config.checkExistence(SETTINGS_FILE, TYPE_FILE) >= EXIST):
			#print 'FOUND SETTING FILE'
			settingsFile = open(SETTINGS_FILE, 'rb') 
			Config.settings = cPickle.load(settingsFile)
			settingsFile.close()
		else:
			#print 'NO SETTING FILE'
			Config.settings = Settings()
			Config.settings.maxConnectionPerFile = MAX_CONN_PER_FILE
			Config.settings.maxConcurrentDownload = MAX_CONC_DOWNLOAD
			Config.settings.resumeSize = RESUME_SIZE * BLK_SIZE
			Config.settings.downloadDir = str(DOWNLOAD_DIR)
			Config.settings.tmpDir = str(TMP_DIR)
			Config.settings.tmpExt = str(TMP_EXT)
			Config.settings.chunkSize = CHUNK_SIZE
			Config.settings.maxConnectionTimeout = MAX_CONNECTION_TIMEOUT
			Config.settings.maxTransferTimeout = MAX_TRANSFER_TIMEOUT
			Config.settings.maxRetry = MAX_RETRY
			Config.settings.cookieFileName = str(COOKIE_FILE)
			Config.settings.reportSize = REPORT_SIZE
			Config.settings.reportDelay = REPORT_DELAY
			Config.settings.queueingListFile = str(QUEUEINGLIST_FILE)			
			Config.settings.useProxy = PROXY
			Config.settings.proxyType = proxyTypeCurlList[proxyTypeList[0]]
			Config.settings.proxyAddr = str(PROXYADDR)
			Config.settings.proxyPort = PROXYPORT
			Config.settings.rapidshareUsername = RAPIDSHARE_USERNAME
			Config.settings.rapidsharePassword = RAPIDSHARE_PASSWORD
			Config.settings.currentId = CURRENT_ID
			Config.settings.cookie = None

		Config.idLock = threading.Lock()	
	
	def save():
		settingsFile = open(SETTINGS_FILE, 'wb') 
		cPickle.dump(Config.settings, settingsFile)
		settingsFile.close()

	def getId():
		Config.idLock.acquire()
		Config.settings.currentId += 1
		Config.idLock.release()
		return Config.settings.currentId
	
	def getFileNameFromURL(fileURL):
		slashPos = fileURL.rfind('/')
		return fileURL[slashPos + 1 :]
		
	def getTmpFile(filename, i):
		tmpFileName = filename + Config.settings.tmpExt + str(i)
		return os.path.join(Config.settings.tmpDir, tmpFileName)

	def checkExistence(object, objectType):
		if (os.access(object, os.W_OK)):
			return EXIST_W
		if (os.access(object, os.R_OK)):
			return EXIST_R			
		if (objectType.upper() == TYPE_FILE):
			if (os.path.isfile(object)):
				return EXIST
		elif (objectType.upper() == TYPE_DIR):
			if (os.path.isdir(object)):
				return EXIST
		
	def catFile(downloadFile):
		desFile = downloadFile.getDestinationFileName()
		if (Config.checkExistence(desFile, TYPE_FILE) > 0):
			#os.remove(desFile)
			return (False, (E_FILEEXIST_CODE, E_FILEEXIST_MSG))
		numberOfPart = downloadFile.getNumberOfPart()
		if (numberOfPart == 1):
			tmpFileName = downloadFile.getFileName() + Config.settings.tmpExt + '0'
			absTmpFileName = os.path.join(Config.settings.tmpDir, tmpFileName)
			cmdMv = 'mv "' + absTmpFileName + '" "' + desFile + '"'
			outPut = commands.getoutput(cmdMv)
			if (outPut.strip() != ''):
				#print 'Error ', outPut.strip()
				return (False, (E_FILEMOVE_CODE, outPut.strip()))
			else:
				#print 'DELETING: ', absTmpFileName
				return (True, None)
			#print 'DELETING: ', absTmpFileName
		else:
			fileNameList = []
			for i in range(0, numberOfPart):
				tmpFileName = downloadFile.getFileName() + Config.settings.tmpExt + str(i)
				absTmpFileName = os.path.join(Config.settings.tmpDir, tmpFileName)
				fileNameList.append(absTmpFileName)
				cmdCat = 'cat "' + absTmpFileName + '" >> "' + desFile + '"'
				#print 'Executing: ' + cmdCat
				outPut = commands.getoutput(cmdCat)
				if (outPut.strip() != ''):
					#print 'Error ', outPut.strip()
					return (False, (E_FILEMOVE_CODE, outPut.strip()))
					
			for absTmpFileName in fileNameList:			
				#print 'DELETING: ', absTmpFileName
				try:
					os.remove(absTmpFileName)
				except OSError, e:
					#print 'Error ', str(e)
					return (False, (E_FILEMOVE_CODE, str(e)))
			return (True, None)

	def checkServerURL(fileURL, serverURL):
		#print 'fileURL : ', fileURL
		if (fileURL.find(HTTP_PRE) != -1):
			serverAdd = fileURL[len(HTTP_PRE) : ]
		elif (fileURL.find(HTTPS_PRE) != -1):
			serverAdd = fileURL[len(HTTPS_PRE) : ]
		else:
			serverAdd = fileURL
		#print 'serverAdd : ', serverAdd
		if (serverAdd.find('/') != -1):
			serverAdd = serverAdd[ : serverAdd.find('/')]
		if (serverAdd.find(serverURL) != -1):
			return True
		else:
			return False
			
	def getLinkType(fileURL, serverURL = None):
		if (fileURL.find(RAPIDSHARE_LINK) != -1):
			return RAPIDSHARE_LINK
		elif (fileURL.find(RAPIDSHARE_FOLDER) != -1):
			return RAPIDSHARE_FOLDER
		else:
			return UNKNOWN_TYPE
		
	
	
	def getPartSize(fileSize, numberOfPart, partNo):
		if (fileSize % numberOfPart == 0):
			partSize = int(fileSize / numberOfPart)
		else:
			partSize = int(floor(fileSize / numberOfPart) + 1)
	
		if (partNo != numberOfPart - 1):			
			return partSize			
		else:
			return int (fileSize - (partNo * partSize))
		
	
	getId = staticmethod(getId)
	getFileNameFromURL = staticmethod(getFileNameFromURL)
	checkExistence = staticmethod(checkExistence)
	getTmpFile = staticmethod(getTmpFile)
	catFile = staticmethod(catFile)
	load = staticmethod(load)
	save = staticmethod(save)
	checkServerURL = staticmethod(checkServerURL)
	getPartSize = staticmethod(getPartSize)
	getLinkType = staticmethod(getLinkType)
	