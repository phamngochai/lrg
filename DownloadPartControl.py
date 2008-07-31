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

#class DownloadPartControl(threading.Thread):
class DownloadPartControl:

	def __init__(self, log, downloadPart, downloadFileControl):
		#threading.Thread.__init__(self)
		self.toContinue = True
		#self.conf = Config()
		self.log = log			
		self.downloadFileControl = downloadFileControl
		self.byteDownloaded = 0
		self.downloadPart = downloadPart
		self.fileObj = None			
		self.reportedTime = 0
		self.toDelete = False
		
		self.curlClass = CurlClass(self.downloadPart.getId())
		self.curl = None
		
	def getDownloadPart(self):
		return self.downloadPart
		
	def stop(self):
		self.toContinue = False
		
	def delete(self):
		if (Config.checkExistence(self.downloadPart.getTmpFileName(), TYPE_FILE) > 0):
			os.remove(self.downloadPart.getTmpFileName())
		self.toDelete = True

	def run(self):
			
		try:
		
			self.downloadPart.setRange()
			
			if (self.downloadPart.isCompleted() == True):
				print 'THIS PART IS COMPLETED, QUIT ', self.downloadPart.getId()
				#self.downloadFileControl.finishPart(self.downloadPart)
				return
			
			tmpFileName = self.downloadPart.getTmpFileName()
			partNo = self.downloadPart.getPartNo()
			currentSize = None
			
			if (self.downloadPart.isResuming()):
				
								
				print 'RESUMING DOWNLOAD ', self.downloadPart.getId()
				self.fileObj = open(tmpFileName, 'r+')
				self.fileObj.seek(self.downloadPart.getFileSeekPos())
				
			else:
				print 'DOWNLOAD NEW ', self.downloadPart.getId()
				self.fileObj = open(tmpFileName, 'w')

			self.curlClass.setDownloadRange(self.downloadPart.getDownloadRange())
			self.curlClass.setFormInfo(self.downloadPart.getFileURL())
			
			if (Config.checkServerURL(self.downloadPart.getFileURL(), RAPIDSHARE)):
				print 'DownloadPartControl Setting cookie ', self.downloadPart.getId()
				self.curlClass.setCookie()
				
			self.curlClass.setProcessBody(self.writeBody)
			self.curlClass.setProgress(self.progressBody)
			#self.curlClass.setControlType(CURL_DLPART)
			self.curlClass.setPartNo(self.downloadPart.getPartNo())
			#print 'Perform now'
			self.curl = self.curlClass.getCurlObject()
			
			print 'DownloadPartControl adding curlObject ', self.curl
			self.downloadFileControl.addCurlObjectToControl(self.curl)
			#print 'DownloadPartControl added curlObject ', self.downloadPart.getId()
		
		except pycurl.error, e:
			print 'DownloadPartControl Exception  ', self.downloadPart.getId(), ' ', pycurl.error, ' ', e
			self.fileObj.flush()
			self.fileObj.close()
				
			#print 'DownloadPartControl pycurl.error:', e
			error = str(e)
			errorCode = int(error[error.find('(') + 1 : error.find(',')])		
			if (errorCode == 23 or errorCode == 42):
				if (self.toDelete):
					os.remove(self.downloadPart.getTmpFileName())
			else:
				errorStr = error[error.find('"') + 1 : error.rfind(')') - 1]				
				self.downloadFileControl.reportError(errorStr)
		except IOError, e:
			if (self.fileObj != None and not self.fileObj.closed):
				self.fileObj.flush()
				self.fileObj.close()		
			self.downloadFileControl.reportError(str(e))
			
			
	def isCompleted(self):
		if (self.downloadPart.isCompleted()):
			#print 'Trying to close from isCompleted ', self.downloadPart.getTmpFileName()
			self.closeTmpFile()
			return True
		else:
			return False
	

	def closeTmpFile(self):
		if (self.fileObj != None and not self.fileObj.closed):
			self.fileObj.flush()
			self.fileObj.close()

			
			
	def writeBody(self, buf):
		if (not self.toContinue or self.toDelete):
			return 1
		try:
			self.fileObj.write(buf)
			self.downloadPart.addByteDownloaded(len(buf))
				
			#print 'partSize ', self.downloadPart.getPartSize(), ' downloaded ', self.downloadPart.getByteDownloaded()
		except IOError, e:
			self.fileObj.flush()
			self.fileObj.close()
			self.downloadFileControl.reportError(str(e))
			print 'DownloadPartControl writeBody IOException: ', self.downloadPart.getId(), ' ', e
			return pycurl.E_WRITE_ERROR
			
	
	def progressBody(self, download_t, download_d, upload_t, upload_d):
		if (not self.toContinue or self.toDelete):
			return 1
		try:
			currentTime = time.time() * 1000		
			timePassed = currentTime - self.reportedTime
			if (timePassed > Config.settings.reportDelay):
				downloadedByte = download_d - self.byteDownloaded
				self.downloadPart.setSpeed((downloadedByte / 1024) / (timePassed / 1000))
				#self.downloadPart.setByteDownloaded(int(download_d))
				#print self.getName(), ' calling report'
				self.downloadFileControl.reportProgress(self.downloadPart)		
				self.reportedTime = currentTime
				self.byteDownloaded = download_d
				
		#What can be wrong here?
		except Exception, e:			
			print 'DownloadPartControl progressBody Exception ', self.downloadPart.getId(), ' ', e
			return 1
	
	