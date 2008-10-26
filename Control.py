import os
import cPickle
import time
import threading
import pycurl

from ConfigUtils import *
from Const import *
from DownloadFileList import DownloadFileList
from DownloadFileControl import DownloadFileControl
from DownloadFile import DownloadFile
from SaveFileControl import SaveFileControl
from Log import Log

from gui.MainFrame import MainFrame

class Control(threading.Thread):
	
	def __init__(self):		
		threading.Thread.__init__(self)
		#Config.load()
		self.saveFileControl = SaveFileControl()
		self.saveFileControl.start()
		self.log = Log()		
		#self.toContinue = True
		self.autoDownload = True
		self.isStopped = False
		self.queueingCurlObjectList = []
		self.curlLock = threading.Lock()
		#Check and load download files list
		if Config.checkExistence(Config.settings.queueingListFile, TYPE_FILE) > NO_EXIST:
			try:
				queueingFile = open(Config.settings.queueingListFile, 'rb')
				self.downloadFileList = cPickle.load(queueingFile)
				queueingFile.close()
			except EOFError:
				self.downloadFileList = DownloadFileList()
				self.log.debug('EXCEPTION Control', EOFError)
				#self.log.debug('Queueing file error')				
			self.downloadFileList.setLock()
			self.downloadFileList.resetStatus(STAT_S)
		else:
			self.downloadFileList = DownloadFileList()
			self.downloadFileList.setLock()		
		
		
		
		#self.mainFrame = MainFrame(None, wx.ID_ANY, "Linux Rapidshare Grabber", (0, 0), (800, 600), self, self.downloadFileList)
		self.mainFrame = None
		
		#show the list in GUI

			
		self.downloadFileControlList = []


	def setMainFrame(self, mainFrame):
		self.mainFrame = mainFrame
		for downloadFile in self.downloadFileList.getList():
			#print downloadFile
			self.mainFrame.addDownloadFileToList(downloadFile, PANEL_TOP)

		for downloadFile in self.downloadFileList.getList(True):
			#print downloadFile
			self.mainFrame.addDownloadFileToList(downloadFile, PANEL_BOT)


	#Add an url to the queueing list
	def addURL(self, fileURL):
		strippedFileURL = str(fileURL).strip()
		if (self.isStopped) or (strippedFileURL == ''):
			return
		if Config.getLinkType(strippedFileURL) == RAPIDSHARE_LINK and strippedFileURL.endswith('.html'):
			strippedFileURL = strippedFileURL[0: len(strippedFileURL) - len('.html')]
		if not self.downloadFileList.getDownloadFileByFileURL(strippedFileURL) is None:
			return MSG_ADD_FILEURL_EXISTED + strippedFileURL
		downloadFile = DownloadFile(strippedFileURL)		
		downloadFile.setId(Config.getId())
		self.downloadFileList.addQueueingFile(downloadFile)		
		self.mainFrame.addDownloadFileToList(downloadFile, PANEL_TOP)
		return MSG_ADD_FILEURL_SUCCESS + strippedFileURL
	
	def addURLById(self, id):
		downloadFile = self.downloadFileList.getDownloadFileById(id, False)
		self.addURL(downloadFile.getFileURL())
	
	#Stop all downloads, save the queueing list then quit
	def exit(self):
		#self.toContinue = False
		self.isStopped = True
		for downloadFileControl in self.downloadFileControlList:
			#print 'Stopping ', downloadFileControl.getDownloadFile().getId()
			downloadFileControl.stop()			
			#print 'Stopping Done'		
		self.downloadFileList.unsetLock()
		#self.log.debug('downloadFileListLock', self.downloadFileList.downloadFileListLock)
		#self.log.debug('completedFileListLock', self.downloadFileList.completedFileListLock)
		self.saveQueueingFiles()
		#for downloadFile in self.downloadFileList.getList():
			#print downloadFile
		Config.save()
		
	#this is dangerous!!!
	def saveQueueingFiles(self):
		queueingFile = open(Config.settings.queueingListFile, 'wb')
		#print dir(self.downloadFileList)
		cPickle.dump(self.downloadFileList, queueingFile, cPickle.HIGHEST_PROTOCOL)
		queueingFile.close()

	
	#add a curl to the curl list
	def addCurlObject(self, curlObject):
		#lockkkk?
		#print 'control addCurlObject getting lock'
		self.curlLock.acquire()
		#print 'adding ', curlObject
		self.queueingCurlObjectList.append(curlObject)
		#print 'control addCurlE_OPERATION_TIMEOUTEDObject releasing lock'
		self.curlLock.release()
		
	#get a curl from the list
	def getCurlObject(self):
		#print 'control getCurlObject getting lock'
		self.curlLock.acquire()
		if len(self.queueingCurlObjectList) != 0:
			curlObject = self.queueingCurlObjectList.pop(0)
			#print 'control getCurlObject releasing lock'
			self.curlLock.release()
			return curlObject
		else:
			#print 'control getCurlObject releasing lock'
			self.curlLock.release()
			return None
			
	#reset the download file		
	def resetDownload(self, id = None):
		if not (id is None):
			found = False
			#self.downloadFileList.changeStatus(fileURL, STAT_S)
			for downloadFileControl in self.downloadFileControlList:
				if downloadFileControl.getDownloadFile().getId() == id:					
					downloadFileControl.resetSettings()
					self.mainFrame.update(downloadFileControl.getDownloadFile(), updateType = [FILESTATUS_COL, RETRY_COL])
					found = True
					break
			if not found:
				downloadFile = self.downloadFileList.getDownloadFileById(id)
				#downloadFile.setStatus(STAT_S)
				downloadFile.resetInfo()
				self.mainFrame.update(downloadFile, updateType = [FILENAME_COL, FILESTATUS_COL])
				

		else:
			#self.isStopped = True
			for downloadFileControl in self.downloadFileControlList:
				#if downloadFileControl.isAlive():
				#downloadFileControl.getDownloadFile().setStatus(STAT_S)				
				downloadFileControl.resetSettings()
				self.mainFrame.update(downloadFileControl.getDownloadFile(), updateType = [FILESTATUS_COL])
		
	
	#stop the download
	def stopDownload(self, id = None):
		if not id is None:
			found = False
			#self.downloadFileList.changeStatus(fileURL, STAT_S)
			for downloadFileControl in self.downloadFileControlList:
				if downloadFileControl.getDownloadFile().getId() == id:					
					downloadFileControl.stop()
					self.mainFrame.update(downloadFileControl.getDownloadFile(), updateType = [FILESTATUS_COL])
					found = True
					downloadFileControl.reset()
					break
			if not found:
				downloadFile = self.downloadFileList.getDownloadFileById(id)
				downloadFile.setStatus(STAT_S)
				self.mainFrame.update(downloadFile, updateType = [FILESTATUS_COL])
				

		else:
			self.autoDownload = False
			for downloadFileControl in self.downloadFileControlList:
				#if downloadFileControl.isAlive():
				#downloadFileControl.getDownloadFile().setStatus(STAT_S)				
				downloadFileControl.stop()
				self.mainFrame.update(downloadFileControl.getDownloadFile(), updateType = [FILESTATUS_COL])
				downloadFileControl.reset()
				
	
	def continueDownload(self, id = None):		
		if not (id is None):
			downloadFile = self.downloadFileList.getDownloadFileById(id)
			if downloadFile.getStatus() != STAT_D:
				downloadFile.setStatus(STAT_Q)
				self.mainFrame.update(downloadFile, updateType = [FILESTATUS_COL])
		else:
			self.downloadFileList.resetStatus(STAT_Q)
			for downloadFile in self.downloadFileList.getList():
				self.mainFrame.update(downloadFile, updateType = [FILESTATUS_COL])
				
		self.autoDownload = True
		
		
	def deleteDownloadTop(self, id = None):
		#print 'deleteDownloadTop ', id
		if not (id is None):
			found = False
			for downloadFileControl in self.downloadFileControlList:
				if downloadFileControl.getDownloadFile().getId() == id:
					found = True
					self.mainFrame.deleteDownloadFileFromList(downloadFileControl.getDownloadFile().getId(), PANEL_TOP)
					downloadFileControl.delete()
					self.downloadFileList.deleteDownloadFileFromDownloadList(downloadFileControl.getDownloadFile().getId())					
			if not found:
				self.downloadFileList.deleteDownloadFileFromDownloadList(id)
				self.mainFrame.deleteDownloadFileFromList(id, PANEL_TOP)
		else:
			self.isStopped = True
			for downloadFileControl in self.downloadFileControlList:
				self.mainFrame.deleteDownloadFileFromList(downloadFileControl.getDownloadFile().getId(), PANEL_TOP)
				downloadFileControl.delete()
				self.downloadFileList.deleteDownloadFileFromDownloadList(downloadFileControl.getDownloadFile().getId())				
			self.downloadFileList.emptyList()
			self.mainFrame.emptyList(PANEL_TOP)
		
		
	def deleteDownloadBot(self, id = None):
		#print 'deleteDownloadBot ', id
		if not (id is None):
			self.mainFrame.deleteDownloadFileFromList(id, PANEL_BOT)
			self.downloadFileList.deleteDownloadFileFromCompletedList(id)
		else:
			self.mainFrame.emptyList(PANEL_BOT)
		

		
	def run(self):
	
		if self.mainFrame is None:
			self.log.debug('No mainFrame found, cannot continue')
			sys.exit()
		
		multiHandler = pycurl.CurlMulti()
		multiHandler.handles = []
		
		i = 0	
			
		#while self.toContinue:
		while not self.isStopped:
				
			#noDFile = self.downloadFileList.getNumberOfDownloadingFile()
			#noQFile = self.downloadFileList.getNumberOfQueueingFile()
			#noQueueingCurlObject = len(self.queueingCurlObjectList)
			maxConn = Config.settings.maxConcurrentDownload
			num_handles = 0
			
			while (not self.isStopped) and (self.autoDownload) and (self.downloadFileList.getNumberOfQueueingFile() > 0):				
				if len(self.downloadFileControlList) < maxConn:
					#and self.downloadFileList.getNumberOfDownloadingFile() < maxConn):
					downloadFile = self.downloadFileList.getQueueingFile()
					if not (downloadFile is None):
						downloadFile.resetRetry()
						
						self.log.debug('Control, Creating:', i, 'instance downloadFileControl', downloadFile.getId(), downloadFile.getFileURL())
						downloadFileControl = DownloadFileControl(self, self.saveFileControl, downloadFile)
						downloadFile.setStatus(STAT_D)
						#downloadFileControl.start()
						downloadFileControl.run()
						self.downloadFileControlList.append(downloadFileControl)				
						i += 1
				else:
					for downloadFileControl in self.downloadFileControlList:
						if downloadFileControl.isDone() and (self.downloadFileList.getNumberOfQueueingFile() > 0):					
							downloadFile = self.downloadFileList.getQueueingFile()
							#print 'Control downloadFile is ', downloadFile
							downloadFileControl.setDownloadFile(downloadFile)
							self.log.debug('Control, Assign downloadFile for downloadFileControl', downloadFile.getId(), downloadFile.getFileURL())
							downloadFileControl.continueBuildCurl()
					break


			#while True:
			while not self.isStopped:
				curlObject = self.getCurlObject()
				if not (curlObject is None):
					multiHandler.add_handle(curlObject)
				else:
					break
					
			#while True:
			while not self.isStopped:
				ret, num_handles = multiHandler.perform()
				if ret != pycurl.E_CALL_MULTI_PERFORM:
					#print 'Perfoming break', ret, ' ', num_handles
					break
				

			#while True:
			while not self.isStopped:
				num_q, ok_list, err_list = multiHandler.info_read()				
				for c in ok_list:
					#c.close()
					multiHandler.remove_handle(c)
					#print 'ok_list removed handle ', c
					httpCode = int(c.getinfo(pycurl.HTTP_CODE))
					#print 'httpCode ', httpCode
					for downloadFileControl in self.downloadFileControlList:
						#print 'Debug ', downloadFileControl
						self.log.debug('Control OK list checking', downloadFileControl.getDownloadFile().getId(), c.downloadFileId)
						if downloadFileControl.getDownloadFile().getId() == c.downloadFileId:
							if not (c.partNo is None):
								self.log.debug('Control curl object belongs to downloadPartControl, checkFinish now')
								downloadFileControl.checkFinish()
								#downloadFileControl.reset()		
								break
								
							if httpCode == 404:
								self.log.debug('Control OK list 404', downloadFileControl.getDownloadFile().getId())
								downloadFileControl.getDownloadFile().setStatus(STAT_E)
								downloadFileControl.getDownloadFile().setErrorStr('404 File not found')
								self.mainFrame.update(downloadFileControl.getDownloadFile())										
								downloadFileControl.reset()
							elif (not downloadFileControl.isDone()) and (not downloadFileControl.isBusy()):								
								self.log.debug('Control OK list continueBuildCurl', downloadFileControl.getDownloadFile().getId())
								downloadFileControl.continueBuildCurl()
							break
   						#print 'Success: ', c.downloadFileId
   					
  				for c, errno, errmsg in err_list:
  					#c.close()
  					multiHandler.remove_handle(c)
  					#print 'err_list removed handle ', c
  					self.log.debug('Control ERROR list error', errno, errmsg)
  					httpCode = int(c.getinfo(pycurl.HTTP_CODE))
  					#print 'err_list httpCode ', httpCode
					for downloadFileControl in self.downloadFileControlList:
						#print 'Debug ', downloadFileControl
						if downloadFileControl.getDownloadFile().getId() == c.downloadFileId:
							self.log.debug('Control ERROR list checking', downloadFileControl.getDownloadFile().getId(), c.downloadFileId)
							if not errno in (pycurl.E_PARTIAL_FILE, pycurl.E_WRITE_ERROR, pycurl.E_ABORTED_BY_CALLBACK):
								self.log.debug('Control ERROR list error unexpected', errno, errmsg)	
								if downloadFileControl.getDownloadFile().isRetryPossible():
									self.log.debug('Control ERROR list retrying')
									downloadFileControl.getDownloadFile().setStatus(STAT_E)
									downloadFileControl.getDownloadFile().setErrorStr(errmsg)
									self.mainFrame.update(downloadFileControl.getDownloadFile(), updateType = [FILESTATUS_COL, FILEERROR_COL])								
									if not (c.partNo is None):
										self.log.debug('Control ERROR list downloadPart failed, resetting part')
										downloadFileControl.resetPart(c.partNo)		
									else:
										self.log.debug('Control ERROR list downloadFile failed, continueBuildCurl')
										downloadFileControl.continueBuildCurl(True)
								else:
									self.log.debug('Control ERROR list no more retry possible, report error')					
									downloadFileControl.reportError(errmsg)
									
								break
														
							if httpCode == 404:
								self.log.debug('Control ERROR list 404')
								downloadFileControl.getDownloadFile().setStatus(STAT_E)
								downloadFileControl.getDownloadFile().setErrorStr('404 File not found')
								self.mainFrame.update(downloadFileControl.getDownloadFile())
								downloadFileControl.reset()
							elif (not downloadFileControl.isDone()) and (not downloadFileControl.isBusy()) and (errno != pycurl.E_ABORTED_BY_CALLBACK):
								self.log.debug('Control ERROR list continueBuildCurl', downloadFileControl.getDownloadFile().getId())
								downloadFileControl.continueBuildCurl()
							break
  					#print 'err_list Failed: ', ' errno ', errno, ' errmsg ', errmsg 
  					#freelist.append(c)
  				#num_processed = num_processed + len(ok_list) + len(err_list)
  				if num_q == 0:
					break

			if num_handles == 0:
				#print 'No more connection, I sleep a bit'
				time.sleep(0.5)
			else:
				ret = multiHandler.select(1.0)
				if ret == -1:
					continue
				#while (True):
				while not self.isStopped:
					ret, num_handles = multiHandler.perform()
					if ret != pycurl.E_CALL_MULTI_PERFORM:
						break
 

			
		for downloadFileControl in self.downloadFileControlList:
			#if (downloadFileControl.isAlive()):
			#	downloadFileControl.join()
			downloadFileControl.kill()
			
		self.mainFrame.quitNow()
		self.saveFileControl.kill()
		self.saveFileControl.join()
		#print 'Control Quit'
	
	def finishFile(self, downloadFile):
		if self.isStopped:
			return
		self.mainFrame.deleteDownloadFileFromList(downloadFile.getId(), PANEL_TOP)
		self.mainFrame.addDownloadFileToList(downloadFile, PANEL_BOT)
		self.downloadFileList.deleteDownloadFileFromDownloadList(downloadFile.getId(), True)
	
	def report(self, downloadFile, updateType):
		if self.isStopped:
			return
		self.mainFrame.update(downloadFile, updateType)


	def printDebug(self):
		print '==================================='
		print 'Total thread: ', threading.activeCount()
		print 'Total downloading File: ', len(self.downloadFileList.getList())
		print 'List download File: '
		for downloadFile in self.downloadFileList.getList():					
			print 'id ', downloadFile.getId(), ' status: ', downloadFile.getStatus()
		print 'List completed File: ', len(self.downloadFileList.getList(True))
		for downloadFile in self.downloadFileList.getList(True):					
			print 'id ', downloadFile.getId(), ' status: ', downloadFile.getStatus()
		print 'List DownloadFileControl: '
		for downloadFileControl in self.downloadFileControlList:
			downloadFile = downloadFileControl.getDownloadFile()			
			print 'id ', downloadFile.getId(), ' busy: ', downloadFileControl.busy, ', done: ', downloadFileControl.done, ', gotJob: ', downloadFileControl.gotJob