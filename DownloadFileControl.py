import socket
import urllib
#import urllib2
import cookielib
import os
import sys
import threading
import time

import pycurl
from math import *

#from getopt import getopt
from LRGParser import LRGParser
#import URLHandlers
from DownloadFile import DownloadFile
from DownloadPart import DownloadPart
from DownloadPartControl import DownloadPartControl
from Log import Log
from Const import *
from ConfigUtils import *
from CurlClass import CurlClass


#class DownloadFileControl(threading.Thread):
class DownloadFileControl:
	def __init__(self, control, saveFileControl, downloadFile = None):
		#threading.Thread.__init__(self)		
		self.log = Log()
		self.isKilled = False
		#self.aLog.info('Starting Download')
		self.control = control
		self.saveFileControl = saveFileControl
		self.downloadFile = downloadFile
		if (self.downloadFile != None):
			#self.downloadFile.setStatus(STAT_D)
			#fileName = Config.getFileNameFromURL(self.downloadFile.getFileURL())
			#self.downloadFile.setFileName(fileName)
			self.downloadFile.increaseRetry()
			#print 'Trying #', self.downloadFile.getRetry(), ' ', self.downloadFile.getId()
			self.control.report(self.downloadFile, updateType = [RETRY_COL])
			#self.isRapidShareLink = self.downloadFile.checkServerURL(RAPIDSHARE)	
			self.curlClass = CurlClass(self.downloadFile.getId())
		else:
			self.curlClass = CurlClass(0)
			
		self.curlObject = None
		self.htmlBody = ''
		self.busy = False
		self.done = False
		self.gotJob = True
		self.downloadPartControlList = []		
		self.isChecking = False
		#self.
		#self.multiCurl = pycurl.CurlMulti()
		#self.multiCurl.handles = []


	def setDownloadFile(self, downloadFile):
		#print 'DownloadFileControl downloadFile is ', downloadFile
		self.downloadFile = downloadFile
		#self.downloadFile.setStatus(STAT_D)
		#fileName = Config.getFileNameFromURL(self.downloadFile.getFileURL())
		#self.downloadFile.setFileName(fileName)
		self.downloadFile.increaseRetry()
		#print 'Trying #', self.downloadFile.getRetry(), ' ', self.downloadFile.getId()
		self.control.report(self.downloadFile, updateType = [RETRY_COL])
		self.htmlBody = ''
		#self.downloadPartControlList = []
		self.isChecking = False
		self.curlClass = CurlClass(self.downloadFile.getId())

	def isBusy(self):
		return self.busy

	def isDone(self):
		return self.done
	
	def continueBuildCurl(self, increaseRetry = False):
		self.gotJob = True
		#self.done = False
		self.busy = True
		if (increaseRetry):
			self.downloadFile.increaseRetry()
			self.control.report(self.downloadFile, updateType = [RETRY_COL])
		self.run()
		
	def reset(self):
		self.busy = False
		self.done = True
		self.gotJob = False

	def stop(self, status = None, toReset = True):
		#self.isKilled = True
		if (status == None):
			self.downloadFile.setStatus(STAT_S)
		else:
			self.downloadFile.setStatus(status)
			
		for downloadPartControl in self.downloadPartControlList:
			downloadPartControl.stop()
		#self.busy = False
		#self.done = True
		#self.gotJob = False
		if (toReset == True):
			self.reset()
			
	def kill(self):
		self.isKilled = True
		self.downloadFile.setStatus(STAT_S)
		for downloadPartControl in self.downloadPartControlList:
			downloadPartControl.stop()		

	def delete(self):
		self.toContinue = False
		for downloadPartControl in self.downloadPartControlList:
			downloadPartControl.delete()
		#self.control.delete(self.downloadFile)
		#self.reset()

	#def setURL(self, aURL):
		#self.aURL = aURL
		#self.load()


	def resetSettings(self):
		self.downloadFile.resetInfo()
		self.stop(STAT_Q, False)
		
		#self.reset()
		self.run()

	def addCurlObjectToControl(self, curlObject):
		self.control.addCurlObject(curlObject)

	def run(self):		
		
		self.log.debug('DownloadFileControl run')
		
		if self.isKilled:
			self.log.debug('DownloadFileControl isKill')
			return
		
		if self.downloadFile is None:
			self.log.debug('DownloadFileControl no downloadFile')
			return
			#continue
			
		if self.gotJob:
			self.done = False
			self.busy = True
			
			try:
				self.htmlBody = '';
				#print 'DownloadFileControl START ', self.downloadFile.getId()
				self.downloadFile.setStatus(STAT_D)
				self.control.report(self.downloadFile, updateType = [FILESTATUS_COL])
				
				#rapidShareLink = Config.checkServerURL(self.downloadFile.getFileURL(), RAPIDSHARE)
				#if (Config.settings.rapidshareUsername == '' and rapidShareLink):
				#	self.downloadFile.setStatus(STAT_E)
				#	self.downloadFile.setErrorStr(MSG_INVALID_USERNAME)
				#	self.control.report(self.downloadFile, updateType = [FILESTATUS_COL, FILEERROR_COL])
				#	self.reset()
				#	return
				#print 'downloadFileControl downloadFile is ', self.downloadFile
				if Config.checkExistence(self.downloadFile.getDestinationFileName(), TYPE_FILE) > 0 :
					self.log.debug('downloadFileControl checkExistence', self.downloadFile.getDestinationFileName(), Config.checkExistence(self.downloadFile.getDestinationFileName(), TYPE_FILE))
					self.downloadFile.setStatus(STAT_X)
					self.control.report(self.downloadFile, updateType = [FILESTATUS_COL])
					self.reset()
					return
					
				#curlClass = CurlClass()
				
				formInfo = self.downloadFile.getFormInfo()			
				if formInfo:
					#print 'GOT FORM ', self.downloadFile.getId()				
					self.curlClass.setFormInfo(self.downloadFile.getFormAction(), formInfo)				
				else:
					#print 'NO FORM ', self.downloadFile.getId()
					self.curlClass.setFormInfo(self.downloadFile.getFileURL())
	
					
				if Config.checkServerURL(self.downloadFile.getFileURL(), RAPIDSHARE) :
					self.curlClass.setCookie()
				
				self.curlClass.setProcessHeader(self.processHeader)
				self.curlClass.setProcessBody(self.processBody)
				self.curlObject = self.curlClass.getCurlObject()
				
				#print 'downloadFileControl adding curl ', self.curlObject
				self.addCurlObjectToControl(self.curlObject)
				
				#print 'DownloadFileControl curlObject added',  self.downloadFile.getId()
				self.gotJob = False
				
			except pycurl.error, e:
				self.log.debug('DownloadFileControl pycurl.error:', e, self.downloadFile.getId())
				error = str(e)
				if error.find('(') == -1 or error.find(',') == -1 :
					return
				errorCode = int(error[error.find('(') + 1 : error.find(',')])
				#print errorCode
				if errorCode == 23 :
					#print '23 is oK, we return'
					return
				else:
					#print 'NOT 23 may restart'
					errorStr = error[error.find('"') + 1 : error.rfind(')') - 1]
					self.downloadFile.setErrorStr(errorStr)
					self.downloadFile.setStatus(STAT_E)
					self.control.report(self.downloadFile, updateType = [FILESTATUS_COL, FILEERROR_COL])
					#if (self.downloadFile.isRetryPossible()):
						#self.downloadFile.increaseRetry()
						#self.run()
					
			except Exception, e:
				self.log.debug('DownloadFileControl Exception:', e, self.downloadFile.getId())
				#print 'DownloadFileControl Exception: ', self.downloadFile.getId(), ' ', e
				#if(self.downloadFile.isRetryPossible()):
					#self.downloadFile.increaseRetry()
					#self.run()			
					#sys.exit(0)
				#else:
					#print 'MAX retry time reached, stop now'
					
			#time.sleep(1.0)
		
	def getDownloadFile(self):
		return self.downloadFile
		

	def fileError(self):
		self.toContinue = False
		self.downloadFile.setStatus(STAT_E)
		#WTF is this???
		self.downloadFile.setErrorStr('File not found')
		self.control.report(self.downloadFile, updateType = [FILESTATUS_COL, FILEERROR_COL])
		
	def reportProgress(self, downloadPart):
		self.control.report(self.downloadFile, updateType = [FILESPEED_COL, FILECOMP_COL])
		
		
	def donePart(self):
		pass

	
	def reportError(self, errorStr, downloadPart = None):
		
		self.downloadFile.setErrorStr(errorStr)
		self.stop(STAT_E)
		self.control.report(self.downloadFile, updateType = [FILESTATUS_COL, FILEERROR_COL])
		
		self.reset()
		#if (downloadPart.isRetryPossible()):
		#	downloadPart.increaseRetry()
		#	downloadPart.setRange()
		#	#print 'DownloadFileCOntrol, timeout, create DownloadPartControl thread'
		#	downloadPartControl = DownloadPartControl(self.log, downloadPart, self)
		#	downloadPartControl.start()
		#	self.downloadPartControlList.append(downloadPartControl)
		#else:
			
		#	print 'MAX RETRY REACHED, abord now ', self.downloadFile.getId()
		
	def resetPart(self, partNo):
		self.downloadFile.setStatus(STAT_D)
		self.downloadFile.setErrorStr('')
		self.downloadFile.increaseRetry()
		self.control.report(self.downloadFile, updateType = [FILESTATUS_COL, RETRY_COL, FILEERROR_COL])
	
		for downloadPartControl in self.downloadPartControlList:
			if downloadPartControl.getDownloadPart().getPartNo() == partNo :
				downloadPartControl.closeTmpFile()
				downloadPartControl.run()
				break
		
		
	def finishPart(self, downloadPart):
		self.checkFinish()

	def checkFinish(self):		
		
		for downloadPartControl in self.downloadPartControlList:			
			if downloadPartControl.isInUse() and not downloadPartControl.isCompleted() :
				return
		if not self.isChecking :
			self.isChecking = True
			#print 'DONE DOWNLOADING ', self.downloadFile.getId()
			self.downloadFile.setStatus(STAT_C)
			self.control.report(self.downloadFile, updateType = [FILESTATUS_COL])
			job = (Config.catFile, self.downloadFile, self.doneSaveFile)
			self.saveFileControl.addJob(job)
		
		
	def doneSaveFile(self, results = None):
		if results:
			result, errors = results
		#print 'CALLBACK FROM SaveFileControl ', self.downloadFile.getId(), ' ', result, ' ', errors
		for downloadPartControl in self.downloadPartControlList:			
			downloadPartControl.resetInUse()
			
		if result:
			self.downloadFile.setStatus(STAT_Z)
			self.control.report(self.downloadFile, updateType = [FILESTATUS_COL])
			self.control.finishFile(self.downloadFile)
			self.reset()
		else:
			errorCode, errorStr = errors 
			self.reportError(errorStr)
			


	def getDownloadPartControl(self):		 	
		for downloadPartControl in self.downloadPartControlList:
			if not downloadPartControl.isInUse() :
				self.log.debug('DownloadFileControl, found DownloadPartControl')
				return downloadPartControl
		self.log.debug('DownloadFileControl, NO DownloadPartControl CAN BE USE, downloadPartControlList is:', len(self.downloadPartControlList))
		return None


	def processTag(self, valList, linksDict):
		formInfo = {}
		action = None
		
		if self.downloadFile.getLinkType() == RAPIDSHARE_FOLDER or self.downloadFile.getLinkType() == URLCASH :
			for link in linksDict.values():
				self.control.addURL(link)
			self.downloadFile.setStatus(STAT_Z)
			self.control.finishFile(self.downloadFile)
			self.reset()
			return
			
		for item in valList:
			for key, value in item.items() :
				if key.find('action') != -1 :
					action = value
					if action.find('/cgi-bin/premium.cgi') != -1 :
						action = 'http://rapidshare.com' + action
				else:
					formInfo[key] = value
		#print 'NEW LINKS: ' + action
		if action :
			self.downloadFile.setFormAction(action)
			self.downloadFile.setFormInfo(formInfo)
			#print 'DownloadFileControl, processTag, create DownloadFileControl thread'
			#download = DownloadFileControl(self.log, self.downloadFile, self.control)
			#download.start()
			#self.downloadFile.setStatus(STAT_D)



	def processHeader(self, buf):
		#print 'Header :', buf
	
		if buf.find(CONTENT_TYPE) != -1 :
			fileType = buf[buf.find(':') + 2 : buf.find(';')]
			self.downloadFile.setFileType(fileType)
			#print 'processHeader, File type: ', fileType
			
		if buf.find(SET_COOKIE) != -1 :
			cookie = buf[buf.find(':') + 2 : buf.find(';')]
			Config.settings.cookie = cookie
			
		if buf.find(CONTENT_LENGTH) != -1 :
			fileSize = int(buf[buf.find(':') + 2 :])
			self.downloadFile.setFileSize(fileSize)
			#print 'processheader, File size: ', fileSize
			
		if buf.find(ACCEPT_RANGE) != 1 :
			self.downloadFile.setResumable(True)

		
	def processBody(self, buf):
		
		if self.downloadFile.getFileType() == TEXTHTML :
			self.htmlBody += buf
			if buf.find('</html>') != -1 :
				toAddPassword = Config.checkServerURL(self.downloadFile.getFileURL(), RAPIDSHARE)
				linkType = self.downloadFile.getLinkType()
				parser = LRGParser(self, toAddPassword, linkType)
				parser.feed(self.htmlBody)
				#print 'DownloadFileControl Parser is done, put busy to False'
				self.busy = False
				#return pycurl.E_WRITE_ERROR
				return 1
		else:
		
			#return pycurl.E_WRITE_ERROR
			
			#print 'DownloadFileControl DONE ', self.downloadFile.getId()
			#self.done = True
						
			#print 'DownloadFileControl OH dear this is: ' + self.downloadFile.getFileType()
			desFile = Config.settings.downloadDir + self.downloadFile.getFileName()
			if Config.checkExistence(desFile, 'F') > 0 :
				#print 'DownloadFileControl FILE EXIST', self.downloadFile.getId()				
				self.control.finishFile(self.downloadFile)
				self.reset()
				return 1
			#if (self.downloadRange == None):				
			#print 'DownloadFileControl GOING TO CREATE THREADS ', self.downloadFile.getId()
			numberOfPart = self.downloadFile.getNumberOfPart()
			#fileSize = self.downloadFile.getFileSize()
			#fileName = self.downloadFile.getFileName()
			
			self.control.report(self.downloadFile, updateType = [FILESIZE_COL])
			
			#if (fileSize % numberOfPart == 0):
			#	partSize = int(fileSize / numberOfPart)
			#else:
			#	partSize = int(floor(fileSize / numberOfPart) + 1)
				
			self.downloadFile.setPartSize()
			
			#self.downloadPartControlList = []
			
			if len(self.downloadFile.getDownloadPartList()) > 0 :
				#print 'Got downloadPartList ', self.downloadFile.getId()
				for downloadPart in self.downloadFile.getDownloadPartList():
					#self.setRange(downloadPart)
					#self.downloadFile.addDownloadPart(downloadPart)
					#print '>>> PART: ', i, ' SIZE on disk: ', currentSize, ' Rollbacksize: ', Config.getResumeSize(), ' RANGE IS: ', dlrange
					#print 'DownloadFileControl, processHeader, create DownloadPartControl Thread'
					downloadPartControl = self.getDownloadPartControl()
					if downloadPartControl is None:
						self.log.debug('DownloadFileControl, no downloadPartControl avail, create new', self.downloadFile.getId())
						downloadPartControl = DownloadPartControl(downloadPart, self)
						self.downloadPartControlList.append(downloadPartControl)
					else:
						downloadPartControl.setDownloadPart(downloadPart)						
					#downloadPartControl.start()
					downloadPartControl.run()										
			
			else:
				#print 'NO downloadPartList ', self.downloadFile.getId()
				for i in range(0, numberOfPart):
					
					downloadPart = DownloadPart(self.downloadFile, i)
					#self.setRange(downloadPart)
					self.downloadFile.addDownloadPart(downloadPart)
					#print '>>> PART: ', i, ' SIZE on disk: ', currentSize, ' Rollbacksize: ', Config.getResumeSize(), ' RANGE IS: ', dlrange
					#print 'DownloadFileControl, processHeader, create DownloadPartControl Thread'
					downloadPartControl = self.getDownloadPartControl()
					if downloadPartControl is None:
						self.log.debug('DownloadFileControl, no downloadPartControl avail, create new', self.downloadFile.getId())
						downloadPartControl = DownloadPartControl(downloadPart, self)
						self.downloadPartControlList.append(downloadPartControl)
					else:
						downloadPartControl.setDownloadPart(downloadPart)
					#downloadPartControl.start()
					downloadPartControl.run()
	
					#self.downloadPartControlList.append(downloadPartControl)

			if self.downloadFile.getStatus() == STAT_S :
				self.stop()
		
			self.checkFinish()		
		
			#return pycurl.E_WRITE_ERROR
			#self.busy = False
			return 1
