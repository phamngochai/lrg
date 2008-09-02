import HTMLParser
from ConfigUtils import *
from Const import *
from Log import Log

class LRGParser(HTMLParser.HTMLParser):
	
	def __init__(self, downloadFileControl, toAddPassword, linkType):	
		HTMLParser.HTMLParser.__init__(self)		
		self.valList = []
		self.toAddPassword = toAddPassword
		self.linkType = linkType
		self.downloadFileControl = downloadFileControl
		self.linksDict = {}
		self.log = Log()
		
	def feed(self, htmlBody):
		try:
			HTMLParser.HTMLParser.feed(self, htmlBody)			
		except HTMLParser.HTMLParseError, e:
			self.log.debug('LRGParser HTMLParser.HTMLParseError', e)
			if self.linkType == URLCASH:
				tmpHTMLBody = htmlBody
				pos = tmpHTMLBody.find(URLCASH_IFRAME)
				if pos != -1:
					tmpBody = tmpHTMLBody[pos + len(URLCASH_IFRAME):]
					rapidUrl = tmpBody[:tmpBody.find(SINGLE_QUOTE)]
					self.log.debug(rapidUrl)
					self.linksDict[rapidUrl] = rapidUrl
					self.downloadFileControl.processTag(self.valList, self.linksDict)
				else:
					self.downloadFileControl.reportError('Cannot find rapidshare links')
		
	def handle_starttag(self, tag, attrs):
		if (tag.find('form') != -1):
			for att in attrs:
				tmpStr = att[0]
				if (tmpStr.find('action') != -1):
					self.valList.append({att[0]: att[1]})
		elif (tag.find('input') != -1):
			foundVar = False
			for att in attrs:
				tupleOne = att[0]
				tupleTwo = att[1]
				if (tupleOne.find('name') != -1):
					if (tupleTwo.find('accountid') != -1 and self.toAddPassword):
						self.valList.append({tupleTwo: Config.settings.rapidshareUsername})
						continue
					if tupleTwo.find('password') != -1:						
						if self.linkType == RAPIDSHARE_FOLDER:							
							downloadFile = self.downloadFileControl.getDownloadFile()
							#print 'Parser password',  downloadFile.getAccessPassword() 
							if downloadFile.getAccessPassword() == '':
								self.downloadFileControl.reportError('This folder needs password to access')
							else:
								self.valList.append({tupleTwo: downloadFile.getAccessPassword()})
							continue
					 	if self.toAddPassword:
							self.valList.append({tupleTwo: Config.settings.rapidsharePassword})
							continue
					name = tupleTwo
					foundVar = True
				elif ((tupleOne.find('value') != -1) and (foundVar) and (tupleTwo.find('Free') == -1)):
					value = tupleTwo
					self.valList.append({name: value})
		elif (tag == 'a'):
			if (self.linkType == RAPIDSHARE_FOLDER):	
				linkProp = {}	 
				for att in attrs:
					linkProp[str(att[0])] = str(att[1])
				#print 'linkProp ', linkProp
				if (linkProp.has_key('style') and linkProp.has_key('target') and linkProp.has_key('href')):
					#print 'style', linkProp['style']
					#print 'target', linkProp['target']
					if (linkProp['style'].find(RAPIDSHARE_STYLE) != 1 and linkProp['target'].find(RAPIDSHARE_TARGET) != -1):
						#print 'adding ', linkProp['href']
						self.linksDict[str(linkProp['href'])] = str(linkProp['href'])
			if (self.linkType == URLCASH):
				#print 'URLCASH'
				#linkProp = {} 
				for att in attrs:
					if (att[0] == 'href' and str(att[1]).find(RAPIDSHARE) != -1):
						#self.linksDict.append(str(att[1]))
						self.linksDict[str(att[1])] = str(att[1])
				

	def handle_endtag(self, tag):
		if (tag.find('html') != -1):
			#if (len(self.valList) > 0):
				#for atts in self.valList:
					#for key, value in atts.items():
						#print key + ': ' + value
			#print 'VALS: ', self.valList
			self.downloadFileControl.processTag(self.valList, self.linksDict)
			#self.callback.processTag(tag, attrs)
			
	def handle_data(self, data):
		for text in errorList:
			if (data.find(text) != -1):
				self.downloadFileControl.reportError(text)
				break