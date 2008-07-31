import os
import threading
import time

class SaveFileControl(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.jobList = []		
		self.toContinue = True
		self.jobLock = threading.Lock()
		
	def addJob(self, job):
		self.jobLock.acquire()
		self.jobList.append(job)
		self.jobLock.release()
		
	
	def kill(self):
		self.toContinue = False
	
	def run(self):
		while (self.toContinue):
			job, args, callback = (None, None, None)
			self.jobLock.acquire()
			if (len(self.jobList) != 0):
				job, args, callback = self.jobList.pop(0)
			self.jobLock.release()
			if (job != None and args != None and callback != None):
				results = job(args)				
				callback(results)
			else:
				time.sleep(0.5)
			