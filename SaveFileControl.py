import os
import threading
import time

class SaveFileControl(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.jobList = []		
		self.toContinue = True
		
	def addJob(self, job):
		self.jobList.append(job)
	
	def kill(self):
		self.toContinue = False
	
	def run(self):
		while (self.toContinue):
			if (len(self.jobList) != 0):
				job, args, callback = self.jobList.pop(0)
				results = job(args)				
				callback(results)
			else:
				time.sleep(0.5)
			