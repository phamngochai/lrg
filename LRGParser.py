from HTMLParser import HTMLParser
from ConfigUtils import *
from Const import *

class LRGParser(HTMLParser):
	
	def __init__(self, downloadFileControl, toAddPassword, linkType):	
		HTMLParser.__init__(self)		
		self.valList = []
		self.toAddPassword = toAddPassword
		self.linkType = linkType
		self.downloadFileControl = downloadFileControl
		self.linkList = []
		
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
					if (tupleTwo.find('password') != -1 and self.toAddPassword):
						self.valList.append({tupleTwo: Config.settings.rapidsharePassword})
						continue
					name = tupleTwo
					foundVar = True
				elif ((tupleOne.find('value') != -1) and (foundVar) and (tupleTwo.find('Free') == -1)):
					value = tupleTwo
					self.valList.append({name: value})
		elif (tag == 'a' and self.linkType == RAPIDSHARE_FOLDER):				
			linkProp = {}			 
			for att in attrs:
				linkProp[str(att[0])] = str(att[1])
			#print 'linkProp ', linkProp
			if (linkProp.has_key('style') and linkProp.has_key('target') and linkProp.has_key('href')):
				#print 'style', linkProp['style']
				#print 'target', linkProp['target']
				if (linkProp['style'].find(RAPIDSHARE_STYLE) != 1 and linkProp['target'].find(RAPIDSHARE_TARGET) != -1):
					#print 'adding ', linkProp['href']
					self.linkList.append(str(linkProp['href']))

	def handle_endtag(self, tag):
		if (tag.find('html') != -1):
			if (len(self.valList) > 0):
				for atts in self.valList:
					for key, value in atts.items():
						print key + ': ' + value
			#print 'VALS: ', self.valList
			self.downloadFileControl.processTag(self.valList, self.linkList)
			#self.callback.processTag(tag, attrs)
			
	def handle_data(self, data):
		for text in errorList:
			if (data.find(text) != -1):
				self.downloadFileControl.reportError(text)
				break