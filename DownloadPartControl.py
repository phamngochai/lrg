import urllib
import urllib2
import pycurl
import threading
import socket
import sys
import time
from ConfigUtils import *
from Const import *
from CurlClass import CurlClass
from Log import Log

#class DownloadPartControl(threading.Thread):
class DownloadPartControl:

	def __init__(self, downloadPart, downloadFileControl):
		#threading.Thread.__init__(self)
		self.toContinue = True
		#self.conf = Config()
		self.log = Log()
		self.downloadFileControl = downloadFileControl
		self.byteDownloaded = 0
		self.downloadPart = downloadPart
		self.fileObj = None
		self.reportedTime = 0
		self.toDelete = False
		self.inUse = True
		
		self.curlClass = CurlClass(self.downloadPart.getId())
		self.log.debug('DownloadPartControl, Created curl object', self.downloadPart.getId())
		self.curl = None

		
	def getDownloadPart(self):
		return self.downloadPart
		
		
	def setDownloadPart(self, downloadPart):
		self.toContinue = True
		self.byteDownloaded = 0
		self.downloadPart = downloadPart
		self.fileObj = None
		self.reportedTime = 0
		self.toDelete = False
		self.inUse = True
		self.curlClass.setDownloadFileId(self.downloadPart.getId())
		
	def stop(self):
		self.toContinue = False
		
	def delete(self):
		if Config.checkExistence(self.downloadPart.getTmpFileName(), TYPE_FILE) > 0 :
			os.remove(self.downloadPart.getTmpFileName())
		self.toDelete = True

	def run(self):
			
		try:
		
			#self.log.debug('DownloadPartControl run')
						
			self.downloadPart.setRange()
			
			if self.downloadPart.isCompleted() :
				self.log.debug('DownloadPartControl THIS PART IS COMPLETED, QUIT', self.downloadPart.getId())
				#self.downloadFileControl.finishPart(self.downloadPart)
				return
			
			tmpFileName = self.downloadPart.getTmpFileName()
			partNo = self.downloadPart.getPartNo()
			currentSize = None
			
			if self.downloadPart.isResuming() :								
				#self.log.debug('RESUMING DOWNLOAD', self.downloadPart.getId())
				self.fileObj = open(tmpFileName, 'r+')
				self.fileObj.seek(self.downloadPart.getFileSeekPos())				
			else:
				#self.log.debug('DOWNLOAD NEW', self.downloadPart.getId())
				self.fileObj = open(tmpFileName, 'w')

			self.curlClass.setDownloadRange(self.downloadPart.getDownloadRange())
			self.curlClass.setFormInfo(self.downloadPart.getFileURL())
			
			if Config.checkServerURL(self.downloadPart.getFileURL(), RAPIDSHARE):
				#print 'DownloadPartControl Setting cookie ', self.downloadPart.getId()
				self.curlClass.setCookie()
				
			self.curlClass.setProcessBody(self.writeBody)
			self.curlClass.setProgress(self.progressBody)
			#self.curlClass.setControlType(CURL_DLPART)
			self.curlClass.setPartNo(self.downloadPart.getPartNo())
			#print 'Perform now'
			self.curl = self.curlClass.getCurlObject()
			
			#print 'DownloadPartControl adding curlObject ', self.curl
			self.downloadFileControl.addCurlObjectToControl(self.curl)
			#print 'DownloadPartControl added curlObject ', self.downloadPart.getId()
		
		except pycurl.error, e:
			self.log.debug('DownloadPartControl Exception pycurl.error', pycurl.error, e, self.downloadPart.getId(),)
			self.fileObj.flush()
			self.fileObj.close()
				
			#print 'DownloadPartControl pycurl.error:', e
			error = str(e)
			errorCode = int(error[error.find('(') + 1 : error.find(',')])		
			if errorCode == 23 or errorCode == 42 :
				if self.toDelete :
					os.remove(self.downloadPart.getTmpFileName())
			else:
				errorStr = error[error.find('"') + 1 : error.rfind(')') - 1]				
				self.downloadFileControl.reportError(errorStr)
		except IOError, e:
			self.log.debug('DownloadPartControl Exception IOError', e, self.downloadPart.getId(),)
			if self.fileObj and not self.fileObj.closed :
				self.fileObj.flush()
				self.fileObj.close()		
			self.downloadFileControl.reportError(str(e))
			
			
	def isCompleted(self):
		if self.downloadPart.isCompleted() :
			self.downloadPart.setSpeed(0)
			#print 'Trying to close from isCompleted ', self.downloadPart.getTmpFileName()
			self.closeTmpFile()
			self.inUse = False
			return True
		else:
			return False
			
			
	def isInUse(self):
		return self.inUse


	def resetInUse(self):
		self.inUse = False
	

	def closeTmpFile(self):
		if self.fileObj and not self.fileObj.closed :
			self.fileObj.flush()
			self.fileObj.close()
			
			
	def writeBody(self, buf):
		if not self.toContinue or self.toDelete :
			return 1
		try:
			if len(buf) == 0:
				self.log.debug('downloadPartControl, this part may be done', self.downloadPart.getId())
			self.fileObj.write(buf)
			self.downloadPart.addByteDownloaded(len(buf))
				
			#print 'partSize ', self.downloadPart.getPartSize(), ' downloaded ', self.downloadPart.getByteDownloaded()
		except IOError, e:
			self.log.debug('downloadPartControl writeBody IOError', e, self.downloadPart.getId())
			self.fileObj.flush()
			self.fileObj.close()
			self.downloadFileControl.reportError(str(e))
			#self.log.debug('DownloadPartControl writeBody IOException:', self.downloadPart.getId(), e)
			return 1
			
	
	def progressBody(self, download_t, download_d, upload_t, upload_d):
		if not self.toContinue or self.toDelete :
			return 1
		try:
			currentTime = time.time() * 1000		
			timePassed = currentTime - self.reportedTime
			if timePassed > Config.settings.reportDelay :
				downloadedByte = download_d - self.byteDownloaded
				self.downloadPart.setSpeed((downloadedByte / 1024) / (timePassed / 1000))
				#self.downloadPart.setByteDownloaded(int(download_d))
				#print self.getName(), ' calling report'
				self.downloadFileControl.reportProgress(self.downloadPart)		
				self.reportedTime = currentTime
				self.byteDownloaded = download_d
				
		#What can be wrong here?
		except Exception, e:			
			self.log.debug('DownloadPartControl progressBody Exception', e, self.downloadPart.getId())
			return 1
	
	