import wx
from gui.MainFrame import MainFrame
from Control import Control
import os
import logging

#pyCurl does not like signal
try:
	import signal
	from signal import SIGPIPE, SIG_IGN
	signal.signal(signal.SIGPIPE, signal.SIG_IGN)
except ImportError:
	pass

logging.basicConfig()
log = logging.getLogger("logger")
log.setLevel(logging.DEBUG)
fh = logging.FileHandler("log.log")
log.addHandler(fh)

app = wx.PySimpleApp()
app.SetAssertMode(wx.PYAPP_ASSERT_DIALOG)

control = Control(log)
control.start()
app.MainLoop()
