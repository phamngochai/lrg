import pycurl
import urllib
from ConfigUtils import *

class CurlClass:
	def __init__(self, downloadFileId = None, debug = None):
		self.curl = pycurl.Curl()
		self.curl.downloadFileId = downloadFileId
		if not debug is None:
			self.curl.setopt(pycurl.VERBOSE, 1)
		else:
			self.curl.setopt(pycurl.VERBOSE, DEBUG)
			
		if Config.settings.useProxy:
			self.curl.setopt(pycurl.PROXY, Config.settings.proxyAddr)
			self.curl.setopt(pycurl.PROXYPORT, Config.settings.proxyPort)			
		
		#self.curl.setopt(pycurl.HTTPHEADER, ['User-Agent: firefox-bin'])
		self.curl.setopt(pycurl.FOLLOWLOCATION, 1)
		self.curl.setopt(pycurl.MAXREDIRS, 5)
		self.curl.setopt(pycurl.NOSIGNAL, 1)
		self.curl.setopt(pycurl.CONNECTTIMEOUT, Config.settings.maxConnectionTimeout)
		self.curl.setopt(pycurl.TIMEOUT, Config.settings.maxTransferTimeout)
		
		#self.curl.controlType = None
		self.curl.partNo = None
		
		
	def setFormInfo(self, formAction, formInfo = None):
		if not formInfo is None:			
			reqParams = urllib.urlencode(formInfo)			
			self.curl.setopt(pycurl.POSTFIELDS, reqParams)				
		self.curl.setopt(pycurl.URL, formAction)

	def setProcessHeader(self, processHeader):	
		self.curl.setopt(pycurl.HEADERFUNCTION, processHeader)
		
	def setProcessBody(self, processBody):
		self.curl.setopt(pycurl.WRITEFUNCTION, processBody)

	def setProgress(self, progressFunction):
		self.curl.setopt(pycurl.NOPROGRESS, 0)
		self.curl.setopt(pycurl.PROGRESSFUNCTION, progressFunction)

	def setResume(self, resumePos):
		#pass
		self.curl.setopt(pycurl.RESUME_FROM, resumePos)
	
	def setDownloadRange(self, range):		
		self.curl.setopt(pycurl.HTTPHEADER, ['User-Agent: firefox-bin', 'Range: bytes=' + range])
	
	def setCookie(self):
		if not Config.settings.cookie is None:
			self.curl.setopt(pycurl.COOKIE, str(Config.settings.cookie))
		#self.curl.setopt(pycurl.COOKIEFILE, Config.settings.cookieFileName)
		#self.curl.setopt(pycurl.COOKIEJAR, Config.settings.cookieFileName)
		
	#def setControlType(self, type):
		#self.curl.controlType = type
		#if type == CURL_DLPART:
			#self.curl.setopt(pycurl.HTTPHEADER, ['Range: firefox-bin'])
	def setDownloadFileId(self, downloadFileId):
		self.curl.downloadFileId = downloadFileId
				
	def setPartNo(self, partNo):
		self.curl.partNo = partNo

	def getCurlObject(self):
		return self.curl