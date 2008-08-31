import logging
import logging.handlers
from Const import *

class Log:
	def __init__(self):
		if DEBUG:
			logging.basicConfig()
		self.log = logging.getLogger("lrg")
		self.log.setLevel(logging.DEBUG)
		self.rotatingFileHandler = logging.handlers.RotatingFileHandler(LOGFILE, 'a', 1000000, 5)
		self.log.addHandler(self.rotatingFileHandler)
	
	def debug(self, *args):
		
		msg = ''
		for arg in args:
			msg += str(arg) + ' '
		if LOG:
			self.log.debug(msg)
		if DEBUG:
			print 'DEBUG: ', msg