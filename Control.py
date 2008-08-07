import os
import cPickle
import time
import wx
import threading
import pycurl

from ConfigUtils import *
from Const import *
from DownloadFileList import DownloadFileList
from DownloadFileControl import DownloadFileControl
from DownloadFile import DownloadFile
from SaveFileControl import SaveFileControl

from gui.MainFrame import MainFrame

class Control(threading.Thread):
	
	def __init__(self, log):
		threading.Thread.__init__(self)
		Config.load()
		self.saveFileControl = SaveFileControl()
		self.saveFileControl.start()
		self.log = log
		self.toContinue = True
		self.isStopped = True
		self.queueingCurlObjectList = []
		self.curlLock = threading.Lock()
		#Check and load download files list
		if (Config.checkExistence(Config.settings.queueingListFile, TYPE_FILE) >= 0):
			queueingFile = open(Config.settings.queueingListFile, 'rb')
			self.downloadFileList = cPickle.load(queueingFile)
			queueingFile.close()
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
		if (not self.toContinue or str(fileURL).strip() == ''):
			return
		downloadFile = DownloadFile(fileURL)		
		downloadFile.setId(Config.getId())
		self.downloadFileList.addQueueingFile(downloadFile)		
		self.mainFrame.addDownloadFileToList(downloadFile, PANEL_TOP)
	
	#Stop all downloads, save the queueing list then quit
	def exit(self):
		self.toContinue = False
		for downloadFileControl in self.downloadFileControlList:
			#print 'Stopping ', downloadFileControl.getDownloadFile().getId()
			downloadFileControl.stop()
			#print 'Stopping Done'
		
		self.downloadFileList.unsetLock()		
		self.saveQueueingFiles()
		#for downloadFile in self.downloadFileList.getList():
			#print downloadFile
		Config.save()
		
	#this is dangerous!!!
	def saveQueueingFiles(self):
		queueingFile = open(Config.settings.queueingListFile, 'wb')
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
		if (len(self.queueingCurlObjectList)):
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
		if (id):
			found = False
			#self.downloadFileList.changeStatus(fileURL, STAT_S)
			for downloadFileControl in self.downloadFileControlList:
				if (downloadFileControl.getDownloadFile().getId() == id):					
					downloadFileControl.resetSettings()
					self.mainFrame.update(downloadFileControl.getDownloadFile(), updateType = [FILESTATUS_COL, RETRY_COL])
					found = True
					break
			if (not found):
				downloadFile = self.downloadFileList.getDownloadFileById(id)
				#downloadFile.setStatus(STAT_S)
				downloadFile.resetInfo()
				self.mainFrame.update(downloadFile, updateType = [FILESTATUS_COL])
				

		else:
			#self.isStopped = True
			for downloadFileControl in self.downloadFileControlList:
				#if (downloadFileControl.isAlive()):
				#downloadFileControl.getDownloadFile().setStatus(STAT_S)				
				downloadFileControl.resetSettings()
				self.mainFrame.update(downloadFileControl.getDownloadFile(), updateType = [FILESTATUS_COL])
		
	
	#stop the download
	def stopDownload(self, id = None):
		if (id):
			found = False
			#self.downloadFileList.changeStatus(fileURL, STAT_S)
			for downloadFileControl in self.downloadFileControlList:
				if (downloadFileControl.getDownloadFile().getId() == id):					
					downloadFileControl.stop()
					self.mainFrame.update(downloadFileControl.getDownloadFile(), updateType = [FILESTATUS_COL])
					found = True
					downloadFileControl.reset()
					break
			if (not found):
				downloadFile = self.downloadFileList.getDownloadFileById(id)
				downloadFile.setStatus(STAT_S)
				self.mainFrame.update(downloadFile, updateType = [FILESTATUS_COL])
				

		else:
			self.isStopped = True
			for downloadFileControl in self.downloadFileControlList:
				#if (downloadFileControl.isAlive()):
				#downloadFileControl.getDownloadFile().setStatus(STAT_S)				
				downloadFileControl.stop()
				self.mainFrame.update(downloadFileControl.getDownloadFile(), updateType = [FILESTATUS_COL])
				downloadFileControl.reset()
				
	
	def continueDownload(self, id = None):		
		if (id):
			downloadFile = self.downloadFileList.getDownloadFileById(id)
			if (downloadFile.getStatus() != STAT_D):
				downloadFile.setStatus(STAT_Q)
				self.mainFrame.update(downloadFile, updateType = [FILESTATUS_COL])
		else:
			self.downloadFileList.resetStatus(STAT_Q)
			for downloadFile in self.downloadFileList.getList():
				self.mainFrame.update(downloadFile, updateType = [FILESTATUS_COL])
				
		self.isStopped = False
		
		
	def deleteDownloadTop(self, id = None):
		print 'deleteDownloadTop ', id
		if (id):
			found = False
			for downloadFileControl in self.downloadFileControlList:
				if (downloadFileControl.getDownloadFile().getId() == id):
					found = True
					self.mainFrame.deleteDownloadFileFromList(downloadFileControl.getDownloadFile().getId(), PANEL_TOP)
					downloadFileControl.delete()
					self.downloadFileList.deleteDownloadFileFromDownloadList(downloadFileControl.getDownloadFile().getId())					
			if (not found):
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
		print 'deleteDownloadBot ', id
		if (id):
			self.mainFrame.deleteDownloadFileFromList(id, PANEL_BOT)
			self.downloadFileList.deleteDownloadFileFromCompletedList(id)
		else:
			self.mainFrame.emptyList(PANEL_BOT)
		

		
	def run(self):
	
		if (self.mainFrame == None):
			print 'No mainFrame found, cannot continue'
			sys.exit()
		
		multiHandler = pycurl.CurlMulti()
		multiHandler.handles = []
		
		i = 0	
			
		while(self.toContinue):
		
			noDFile = self.downloadFileList.getNumberOfDownloadingFile()
			noQFile = self.downloadFileList.getNumberOfQueueingFile()
			noQueueingCurlObject = len(self.queueingCurlObjectList)		
			maxConn = Config.settings.maxConcurrentDownload
			
			while (not self.isStopped and self.downloadFileList.getNumberOfQueueingFile() > 0):
				if (len(self.downloadFileControlList) < maxConn):		
					#and self.downloadFileList.getNumberOfDownloadingFile() < maxConn):
					downloadFile = self.downloadFileList.getQueueingFile()
					if (downloadFile != None):
						downloadFile.resetRetry()
						
						print 'Creating: ', i , ' instance ', downloadFile.getId(), ' ', downloadFile.getFileURL()
						downloadFileControl = DownloadFileControl(self.log, self, self.saveFileControl, downloadFile)
						downloadFile.setStatus(STAT_D)
						#downloadFileControl.start()
						downloadFileControl.run()
						self.downloadFileControlList.append(downloadFileControl)				
						i += 1
				else:
					for downloadFileControl in self.downloadFileControlList:
						if (downloadFileControl.isDone() and self.downloadFileList.getNumberOfQueueingFile() > 0):					
							downloadFile = self.downloadFileList.getQueueingFile()
							#print 'Control downloadFile is ', downloadFile
							downloadFileControl.setDownloadFile(downloadFile)
							print 'New downloadFile for downloadFileControl ', downloadFileControl.getDownloadFile().getId()
							downloadFileControl.continueBuildCurl()
					break


			while (True):
				curlObject = self.getCurlObject()
				if (curlObject != None):
					multiHandler.add_handle(curlObject)
				else:
					break
					
			while (True):
				ret, num_handles = multiHandler.perform()
				if ret != pycurl.E_CALL_MULTI_PERFORM:
					#print 'Perfoming break', ret, ' ', num_handles
					break

			while (True):
			
				num_q, ok_list, err_list = multiHandler.info_read()
				
				for c in ok_list:
					#c.close()
					multiHandler.remove_handle(c)
					#print 'ok_list removed handle ', c
					httpCode = int(c.getinfo(pycurl.HTTP_CODE))
					#print 'httpCode ', httpCode
					for downloadFileControl in self.downloadFileControlList:
						#print 'Debug ', downloadFileControl
						#print 'Checking ', downloadFileControl.getDownloadFile().getId(), ' ', c.downloadFileId
						if (downloadFileControl.getDownloadFile().getId() == c.downloadFileId):
							if (c.partNo != None):
								downloadFileControl.checkFinish()
								#downloadFileControl.reset()		
								break
								
							if (httpCode == 404):
								#print 'Success Reseting 404', downloadFileControl.getDownloadFile().getId()
								downloadFileControl.getDownloadFile().setStatus(STAT_E)
								downloadFileControl.getDownloadFile().setErrorStr('404 File not found')
								self.mainFrame.update(downloadFileControl.getDownloadFile())										
								downloadFileControl.reset()
							elif (downloadFileControl.isDone() == False	and  downloadFileControl.isBusy() == False):								
								#print 'Success Continue ', downloadFileControl.getDownloadFile().getId()
								downloadFileControl.continueBuildCurl()
							break
   						#print 'Success: ', c.downloadFileId
   					
  				for c, errno, errmsg in err_list:
  					#c.close()
  					multiHandler.remove_handle(c)
  					#print 'err_list removed handle ', c
  					httpCode = int(c.getinfo(pycurl.HTTP_CODE))
  					#print 'err_list httpCode ', httpCode
					for downloadFileControl in self.downloadFileControlList:
						#print 'Debug ', downloadFileControl
						if (downloadFileControl.getDownloadFile().getId() == c.downloadFileId):						

							if (not errno in (pycurl.E_ABORTED_BY_CALLBACK, pycurl.E_PARTIAL_FILE, pycurl.E_WRITE_ERROR)):				
								if (downloadFileControl.getDownloadFile().isRetryPossible()):
									downloadFileControl.getDownloadFile().setStatus(STAT_E)
									downloadFileControl.getDownloadFile().setErrorStr(errmsg)
									self.mainFrame.update(downloadFileControl.getDownloadFile(), updateType = [FILESTATUS_COL, FILEERROR_COL])								
									if (c.partNo != None):
										#print 'downloadPart failed, resetitng part'
										downloadFileControl.resetPart(c.partNo)		
									else:
										#print 'downloadFile failed, resetitng file'
										downloadFileControl.continueBuildCurl(True)

								else:						
									downloadFileControl.reportError(errmsg)
									
								break
														
							if (httpCode == 404):
								#print 'Fail resetting 404'
								downloadFileControl.getDownloadFile().setStatus(STAT_E)
								downloadFileControl.getDownloadFile().setErrorStr('404 File not found')
								self.mainFrame.update(downloadFileControl.getDownloadFile())
								downloadFileControl.reset()
							elif (downloadFileControl.isDone() == False and  downloadFileControl.isBusy() == False):
								#print 'err_list Fail curlObject ', downloadFileControl.getDownloadFile().getId(), ' errno ', errno, ' errmsg ', errmsg
								downloadFileControl.continueBuildCurl()
							break
  					#print 'err_list Failed: ', ' errno ', errno, ' errmsg ', errmsg 
  					#freelist.append(c)
  				#num_processed = num_processed + len(ok_list) + len(err_list)
  				if num_q == 0:
					break

			if (num_handles == 0):
				#print 'No more connection, I sleep a bit'
				time.sleep(0.5)
			else:
				multiHandler.select(1.0)

			
		for downloadFileControl in self.downloadFileControlList:
			#if (downloadFileControl.isAlive()):
			#	downloadFileControl.join()
			downloadFileControl.kill()
			
		self.mainFrame.quitNow()
		self.saveFileControl.kill()
		self.saveFileControl.join()
		#print 'Control Quit'
	
	def finishFile(self, downloadFile):
		if (not self.toContinue):
			return
		self.mainFrame.deleteDownloadFileFromList(downloadFile.getId(), PANEL_TOP)
		self.mainFrame.addDownloadFileToList(downloadFile, PANEL_BOT)
		self.downloadFileList.deleteDownloadFileFromDownloadList(downloadFile.getId(), True)
	
	def report(self, downloadFile, updateType):
		if (not self.toContinue):
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