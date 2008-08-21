import logging
from Const import *

class Log:
	def __init__(self):
		logging.basicConfig()
		self.log = logging.getLogger("lrg")
		self.log.setLevel(logging.DEBUG)
		self.fileHandler = logging.FileHandler(LOGFILE)
		self.log.addHandler(self.fileHandler)
	
	def doLog(self, *args):
		if (LOG):
			msg = ''
			for arg in args:
				msg += str(arg)
			self.log.debug(msg)