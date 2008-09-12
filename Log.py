import logging
import logging.handlers
from Const import *

class Log:

	log = None
	rotatingFileHandler = None
	
	def __init__(self):
		if DEBUG:
			logging.basicConfig()
		if not Log.log:
			Log.log = logging.getLogger("lrg")
			Log.log.setLevel(logging.DEBUG)
			Log.rotatingFileHandler = logging.handlers.RotatingFileHandler(LOGFILE, 'a', 1000000, 5)
			Log.log.addHandler(Log.rotatingFileHandler)
	
	def debug(self, *args):
		
		msg = ''
		for arg in args:
			msg += str(arg) + ' '
		if LOG:
			Log.log.debug(msg)
		if DEBUG:
			print 'DEBUG: ', msg