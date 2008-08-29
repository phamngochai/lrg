import wx
import os
import logging
import time
from gui.MainFrame import MainFrame
from Const import *
from Control import Control
from ConfigUtils import Config
from Log import Log

#pyCurl does not like signal
log = Log()
try:
	import signal
	from signal import SIGPIPE, SIG_IGN
	signal.signal(signal.SIGPIPE, signal.SIG_IGN)
except ImportError, e:
	log.debug('Main ImportError', e)
	print 'Cannot handle signal...'
	
Config.load()

app = wx.PySimpleApp()
app.SetAssertMode(wx.PYAPP_ASSERT_DIALOG)

control = Control()
mainFrame = MainFrame(None, wx.ID_ANY, "Linux Rapidshare Grabber", (0, 0), (800, 600), control)
control.setMainFrame(mainFrame)
control.start()
app.MainLoop()
