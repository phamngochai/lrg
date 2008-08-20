import wx
import os
import time
from PanelTop import PanelTop
from PanelBot import PanelBot
from TextBox import TextBox
from ConfigBox import ConfigBox
from AboutBox import AboutBox
from DownloadFilePropBox import DownloadFilePropBox
from Const import *
import threading

ID_OPEN = 1001
ID_PASTE = 1002
ID_EXIT = 1003

ID_SETTING = 1004

ID_ABORT = 1005
ID_START = 1006
ID_DELET = 1007

ID_ABOUT = 2001
ID_HELP = 2002

ID_STOP_POP_TOP = 3001
ID_CONT_POP_TOP = 3002
ID_RESE_POP_TOP = 3003
ID_DELE_POP_TOP = 3004
ID_PROP_POP_TOP = 3005


ID_REDO_POP_BOT = 4001
ID_DELE_POP_BOT = 4002


class MainFrame(wx.Frame):
	def __init__(self, parent, id, title, pos, size, control):
		wx.Frame.__init__(self, parent, id, title, pos, size)
		
		self.control = control
		self.configBox = None
		self.textBox = None
		self.aboutBox = None
		self.fileDialog = None
		self.downloadFilePropBox = None
		
		self.selectedIds = []
		self.CreateStatusBar()
		
		self.fileMenu = wx.Menu()
		self.fileMenu.Append(ID_OPEN, '&Open links from file', 'Open links from file')
		self.fileMenu.Append(ID_PASTE, '&Paste links from clipboard', 'Paste links from clipboard')
		self.fileMenu.AppendSeparator()
		self.fileMenu.Append(ID_EXIT,'E&xit', 'Terminate the program')

		self.editMenu = wx.Menu()
		self.editMenu.Append(ID_SETTING, '&Settings', 'Settings')
		
		self.actionMenu = wx.Menu()
		self.actionMenu.Append(ID_ABORT, '&Abort all', 'Abort all')
		self.actionMenu.Append(ID_START, '&Start all', 'Start all')
		self.actionMenu.Append(ID_DELET, '&Delete all', 'Delete all')
		
		self.helpMenu = wx.Menu()
		self.helpMenu.Append(ID_HELP, '&Help', 'RTFM')
		self.helpMenu.AppendSeparator()
		self.helpMenu.Append(ID_ABOUT, 'About &LRG', 'General info about lrg')
		
		
		self.menuBar = wx.MenuBar()
		
		self.menuBar.Append(self.fileMenu, '&File')
		self.menuBar.Append(self.editMenu, '&Edit')
		self.menuBar.Append(self.actionMenu, '&Action')
		self.menuBar.Append(self.helpMenu, '&Help')
		self.SetMenuBar(self.menuBar)

		self.topPopupMenu = wx.Menu()
		self.topPopupMenu.Append(ID_STOP_POP_TOP, 'Sto&p', 'Stop')
		self.topPopupMenu.Append(ID_CONT_POP_TOP, '&Start/Continue', 'Start/Continue')
		self.topPopupMenu.Append(ID_RESE_POP_TOP, '&Reset', 'Reset')
		self.topPopupMenu.Append(ID_DELE_POP_TOP, '&Delete', 'Delete')
		self.topPopupMenu.Append(ID_PROP_POP_TOP, '&Properties', 'Properties')
		
		self.botPopupMenu = wx.Menu()
		self.botPopupMenu.Append(ID_REDO_POP_BOT, '&Redownload', 'Redownload')
		self.botPopupMenu.Append(ID_DELE_POP_BOT, '&Delete', 'Delete')
	
		
		
		wx.EVT_MENU(self, ID_PASTE, self.onPaste)
		wx.EVT_MENU(self, ID_OPEN, self.onOpen)
		wx.EVT_MENU(self, ID_SETTING, self.onConfig)
		wx.EVT_MENU(self, ID_ABORT, self.onAbortAll)
		wx.EVT_MENU(self, ID_START, self.onStartAll)
		wx.EVT_MENU(self, ID_DELET, self.onDeleteAll)
		wx.EVT_MENU(self, ID_STOP_POP_TOP, self.onStop)
		wx.EVT_MENU(self, ID_CONT_POP_TOP, self.onContinue)
		wx.EVT_MENU(self, ID_RESE_POP_TOP, self.onResetDownload)		
		wx.EVT_MENU(self, ID_DELE_POP_TOP, self.onDeleteTop)
		wx.EVT_MENU(self, ID_PROP_POP_TOP, self.onDownloadFileProp)		
		wx.EVT_MENU(self, ID_REDO_POP_BOT, self.onRedownload)
		wx.EVT_MENU(self, ID_DELE_POP_BOT, self.onDeleteBot)
		
		
		wx.EVT_MENU(self, ID_HELP, self.onHelp)		
		
		wx.EVT_MENU(self, ID_EXIT, self.onExit)
		wx.EVT_MENU(self, ID_ABOUT, self.onAbout)
		
		wx.EVT_CLOSE(self, self.onExit)
		
		self.splitter = wx.SplitterWindow(self, wx.ID_ANY)
		self.splitter.SetBorderSize(20)
		self.panelTop = PanelTop(self.splitter, wx.ID_ANY, self.popupMenuCallback)
		self.panelBot = PanelBot(self.splitter, wx.ID_ANY, self.popupMenuCallback)
		self.splitter.SplitHorizontally(self.panelTop, self.panelBot)
		
		self.sizerContainer = wx.BoxSizer(wx.VERTICAL)
		self.sizerContainer.Add(self.splitter, 1, wx.EXPAND)
	
		self.SetSizer(self.sizerContainer)	
		self.SetAutoLayout(True)		
		
		self.Show(True)
		
		
	def onHelp(self, event):		
		self.control.printDebug()
		
	def onPaste(self, event):
		if (self.textBox):
			self.textBox.Show()
		else:
			self.textBox = TextBox(self, wx.ID_ANY, 'Please enter text', pos = (0, 0), size = (500,300), callback = self.enterLinks)

		
	def onOpen(self, event):
		self.dirName = ''
		self.fileName = ''
		if (self.fileDialog):
			self.fileDialog.show()
		else:
			self.fileDialog = wx.FileDialog(self, 'Please select a text file', self.dirName, '', '*.*', wx.OPEN)
			if self.fileDialog.ShowModal() == wx.ID_OK:
				self.fileName = self.fileDialog.GetDirectory() + '/'+ self.fileDialog.GetFilename()
				urlFile = open(self.fileName, 'r')
				for url in urlFile.readlines():
					if (url.strip() != ''):
						self.control.addURL(url.strip())
			self.fileDialog.Destroy()
			
	def onAbout(self, event):
		#print 'Total threads: ', threading.activeCount()
		if (self.aboutBox):
			self.aboutBox.Show(True)
		else:
			self.aboutBox = AboutBox(self, wx.ID_ANY, 'About')
		
	def popupMenuCallback(self, selectedIds, position, PanelPos):
		#print selectedRows
		#print event
		self.selectedIds = selectedIds
		if (PanelPos == PANEL_TOP):
			if (len(self.selectedIds)  == 1):
				self.topPopupMenu.Enable(ID_PROP_POP_TOP, True)
			else:
				self.topPopupMenu.Enable(ID_PROP_POP_TOP, False)
			self.panelTop.PopupMenu(self.topPopupMenu, position)
		else:
			self.panelBot.PopupMenu(self.botPopupMenu, position)

		
	def enterLinks(self, links):
		#print links
		urlList = links.split()
		for url in urlList:
			#for url in urls.split(" "):
			if (url.strip() != ''):
				self.control.addURL(url.strip())

		
		
	def onConfig(self, event):
		if (self.configBox):
			self.configBox.Show(True)
		else:
			self.configBox = ConfigBox(self, wx.ID_ANY, 'Settings')
					

	def onAbortAll(self, event):
		self.control.stopDownload()


	def onStop(self, event):
		for id in self.selectedIds:
			self.control.stopDownload(id)
			
			
	def onStartAll(self, event):
		self.control.continueDownload()
		
		
	def onContinue(self, event):
		for id in self.selectedIds:
			self.control.continueDownload(id)


	def onResetDownload(self, event):
		for id in self.selectedIds:
			self.control.resetDownload(id)


	def onDeleteTop(self, event):
		#print self.selectedIds
		for id in self.selectedIds:
			self.control.deleteDownloadTop(id)
		
		
	def onDeleteAll(self, event):
		self.control.deleteDownloadTop()
					

	def onRedownload(self, event):
		for id in self.selectedIds:
			self.control.addURL(id)
					

	def onDeleteBot(self, event):
		for id in self.selectedIds:
			self.control.deleteDownloadBot(id)

	def onDownloadFileProp(self, event):					
		if (self.downloadFilePropBox):
			if (self.downloadFilePropBox.getDownloadFileId() != self.selectedIds[0]):
				downloadFile = self.control.downloadFileList.getDownloadFileById(self.selectedIds[0])
				self.downloadFilePropBox.setDownloadFile(downloadFile)
			wx.CallAfter(self.downloadFilePropBox.updateInfo)
			self.downloadFilePropBox.Show(True)			
		else:
			#print 'self.selectedURLS ', self.selectedURLS
			downloadFile = self.control.downloadFileList.getDownloadFileById(self.selectedIds[0])
			self.downloadFilePropBox = DownloadFilePropBox(self, wx.ID_ANY, 'Properties', downloadFile)
		
	
		
	def setSelectedIds(self, selectedIds):
		self.selectedIds = selectedIds
		
		
	def onExit(self, event):
		self.control.exit()
		
		
	def quitNow(self):
		self.Destroy()
		

	def update(self, downloadFile, updateType):		
		wx.CallAfter(self.panelTop.update, downloadFile, updateType)
		if (self.downloadFilePropBox and self.downloadFilePropBox.getDownloadFileId() == downloadFile.getId()):
			wx.CallAfter(self.downloadFilePropBox.updateInfo)
		
	def addDownloadFileToList(self, downloadFile, panelPos):
		if (panelPos == PANEL_TOP):
			wx.CallAfter(self.panelTop.addDownloadFile, downloadFile)
		else:
			wx.CallAfter(self.panelBot.addDownloadFile, downloadFile)		

	def deleteDownloadFileFromList(self, id, panelPos):
		if (panelPos == PANEL_TOP):
			wx.CallAfter(self.panelTop.deleteDownloadFile, id)
		else:
			wx.CallAfter(self.panelBot.deleteDownloadFile, id)
		
		
	def emptyList(self, panelPos):
		if (panelPos == PANEL_TOP):		
			wx.CallAfter(self.panelTop.deleteAllDownloadFile)
		else:
			wx.CallAfter(self.panelBop.deleteAllDownloadFile)
