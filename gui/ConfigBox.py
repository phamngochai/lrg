import wx
from ConfigUtils import *

ID_TMPDIR_BUT = 81001
ID_INDIR_BUT = 81002

ID_OK_BUT = 82001
ID_CLOSE_BUT = 82002

PADDING = 10



class ConfigBox(wx.Frame):

	def __init__(self, parent, id, title):
		wx.Frame.__init__(self, parent, id, title, style = wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | wx.MINIMIZE_BOX | wx.RESIZE_BOX | wx.MAXIMIZE_BOX))
		
		self.incomingDirDialog = None
		self.tmpDirDialog = None

		self.splitter = wx.SplitterWindow(self, wx.ID_ANY)
		self.splitter.SetBorderSize(0)
		
		self.noteBookPanel = wx.Panel(self.splitter, wx.ID_ANY)
		self.noteBook = wx.Notebook(self.noteBookPanel)	
		self.mainSizer = wx.BoxSizer(wx.VERTICAL)		
		
		self.generalSettingsPanel = wx.Panel(self.noteBook, wx.ID_ANY)
		
		self.generalSettingsSizer = wx.BoxSizer(wx.VERTICAL)		
		
		self.rapidAccountBox = wx.StaticBox(self.generalSettingsPanel, label='Account Settings')
		self.rapidAccountBoxSizer = wx.StaticBoxSizer(self.rapidAccountBox, wx.VERTICAL)
		
		self.usernameLbl = wx.StaticText(self.generalSettingsPanel, wx.ID_ANY, 'Rapidshare username:')		
		self.username = wx.TextCtrl(self.generalSettingsPanel, wx.ID_ANY)
		self.username.SetValue(Config.settings.rapidshareUsername)
		self.passwordLbl = wx.StaticText(self.generalSettingsPanel, wx.ID_ANY, 'Rapidshare password:')
		self.password = wx.TextCtrl(self.generalSettingsPanel, wx.ID_ANY)
		self.password.SetValue(Config.settings.rapidsharePassword)		
		
		self.rapidAccountBoxSizer.Add(self.usernameLbl, 0, wx.ALL, PADDING)
		self.rapidAccountBoxSizer.Add(self.username, 0, wx.EXPAND)
		self.rapidAccountBoxSizer.Add(self.passwordLbl, 0, wx.ALL, PADDING)
		self.rapidAccountBoxSizer.Add(self.password, 0, wx.EXPAND)

		self.generalSettingsSizer.Add(self.rapidAccountBoxSizer, 0, wx.EXPAND)
		
		self.directoryBox = wx.StaticBox(self.generalSettingsPanel, label='Directory settings')
		self.directoryBoxSizer = wx.StaticBoxSizer(self.directoryBox, wx.VERTICAL)
		
		self.incomingDirLbl = wx.StaticText(self.generalSettingsPanel, wx.ID_ANY, 'Incoming directory:')
		self.incomingDir = wx.TextCtrl(self.generalSettingsPanel, wx.ID_ANY)
		self.incomingDir.SetValue(Config.settings.downloadDir)
		self.incomingBut = wx.Button(self.generalSettingsPanel, ID_INDIR_BUT, 'Browse')
		wx.EVT_BUTTON(self, ID_INDIR_BUT, self.onSelectIncomingDir)
		
		self.incomingDirSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.incomingDirSizer.Add(self.incomingDir, 3, wx.EXPAND, PADDING)
		self.incomingDirSizer.Add(self.incomingBut, 0, wx.EXPAND, PADDING)
	
		self.tmpDirLbl = wx.StaticText(self.generalSettingsPanel, wx.ID_ANY, 'Temporary directory:')
		self.tmpDir = wx.TextCtrl(self.generalSettingsPanel, wx.ID_ANY)
		self.tmpDir.SetValue(Config.settings.tmpDir)
		self.tmpBut = wx.Button(self.generalSettingsPanel, ID_TMPDIR_BUT, 'Browse')
		wx.EVT_BUTTON(self, ID_TMPDIR_BUT, self.onSelectTmpDir)
		
		self.tmpDirSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.tmpDirSizer.Add(self.tmpDir, 3, wx.EXPAND, PADDING)
		self.tmpDirSizer.Add(self.tmpBut, 0, wx.EXPAND, PADDING)
		
		
		self.directoryBoxSizer.Add(self.incomingDirLbl, 0, wx.ALL, PADDING)
		self.directoryBoxSizer.Add(self.incomingDirSizer, 0, wx.EXPAND)
		self.directoryBoxSizer.Add(self.tmpDirLbl, 0, wx.ALL, PADDING)
		self.directoryBoxSizer.Add(self.tmpDirSizer, 0, wx.EXPAND)
		
		self.generalSettingsSizer.Add(self.directoryBoxSizer, 0, wx.EXPAND)
			
		self.generalSettingsPanel.SetSizerAndFit(self.generalSettingsSizer)		
		self.generalSettingsPanel.SetAutoLayout(True)
		self.generalSettingsPanel.Layout()	
	
	

		self.networkSettingsPanel = wx.Panel(self.noteBook, wx.ID_ANY)
		
		self.networkSettingsSizer = wx.BoxSizer(wx.VERTICAL)		
		
		self.networkSettingsBox = wx.StaticBox(self.networkSettingsPanel, label='General Settings')
		self.networkSettingsBoxSizer = wx.StaticBoxSizer(self.networkSettingsBox, wx.VERTICAL)
		
		self.numberOfConnSizer = wx.BoxSizer(wx.HORIZONTAL)		
		self.numberOfConnLbl = wx.StaticText(self.networkSettingsPanel, wx.ID_ANY, 'Number of concurent file:')		
		self.numberOfConn = wx.TextCtrl(self.networkSettingsPanel, wx.ID_ANY)
		self.numberOfConn.SetValue(str(Config.settings.maxConcurrentDownload))
		self.numberOfConnSizer.Add(self.numberOfConnLbl, 0, wx.ALL, PADDING)
		self.numberOfConnSizer.Add(self.numberOfConn, 0, wx.ALL)
		
		
		self.numberOfConnPerFileSizer = wx.BoxSizer(wx.HORIZONTAL)		
		self.numberOfConnPerFileLbl = wx.StaticText(self.networkSettingsPanel, wx.ID_ANY, 'Number of concurent per file:')
		self.numberOfConnPerFile = wx.TextCtrl(self.networkSettingsPanel, wx.ID_ANY)
		self.numberOfConnPerFile.SetValue(str(Config.settings.maxConnectionPerFile))
		self.numberOfConnPerFileSizer.Add(self.numberOfConnPerFileLbl, 0, wx.ALL, PADDING)
		self.numberOfConnPerFileSizer.Add(self.numberOfConnPerFile, 0, wx.ALL)

		self.maxRetrySizer = wx.BoxSizer(wx.HORIZONTAL)		
		self.maxRetryLbl = wx.StaticText(self.networkSettingsPanel, wx.ID_ANY, 'Max retry:')
		self.maxRetry = wx.TextCtrl(self.networkSettingsPanel, wx.ID_ANY)
		self.maxRetry.SetValue(str(Config.settings.maxRetry))
		self.maxRetrySizer.Add(self.maxRetryLbl, 0, wx.ALL, PADDING)
		self.maxRetrySizer.Add(self.maxRetry, 0, wx.ALL)


		self.networkSettingsBoxSizer.Add(self.numberOfConnSizer, 0, wx.EXPAND)
		self.networkSettingsBoxSizer.Add(self.numberOfConnPerFileSizer, 0, wx.EXPAND)
		self.networkSettingsBoxSizer.Add(self.maxRetrySizer, 0, wx.EXPAND)

		self.networkSettingsSizer.Add(self.networkSettingsBoxSizer, 0, wx.EXPAND, PADDING)	
	

		self.proxyBox = wx.StaticBox(self.networkSettingsPanel, label='Proxy settings')
		self.proxyBoxSizer = wx.StaticBoxSizer(self.proxyBox, wx.VERTICAL)
		
		self.useProxy = wx.CheckBox(self.networkSettingsPanel, -1, 'Use proxy')
		self.useProxy.SetValue(Config.settings.useProxy)
		
		self.proxyTypeSizer = wx.BoxSizer(wx.VERTICAL)
		self.proxyTypeLbl = wx.StaticText(self.networkSettingsPanel, wx.ID_ANY, 'Type:')
		self.proxyTypeList = wx.ComboBox(self.networkSettingsPanel, wx.ID_ANY, value = proxyTypeList[0], choices = proxyTypeList, style = wx.CB_READONLY)
		self.proxyTypeList.SetStringSelection(proxyTypeValueList[Config.settings.proxyType])
		self.proxyTypeSizer.Add(self.proxyTypeLbl, 0, wx.EXPAND)
		self.proxyTypeSizer.Add(self.proxyTypeList, 0, wx.EXPAND)

		self.proxyAddrSizer = wx.BoxSizer(wx.VERTICAL)
		self.proxyAddrLbl = wx.StaticText(self.networkSettingsPanel, wx.ID_ANY, 'Address:')
		self.proxyAddr = wx.TextCtrl(self.networkSettingsPanel, wx.ID_ANY)
		self.proxyAddr.SetValue(str(Config.settings.proxyAddr))
		self.proxyAddrSizer.Add(self.proxyAddrLbl, 0, wx.EXPAND)
		self.proxyAddrSizer.Add(self.proxyAddr, 0, wx.EXPAND)

		self.proxyPortSizer = wx.BoxSizer(wx.VERTICAL)
		self.proxyPortLbl = wx.StaticText(self.networkSettingsPanel, wx.ID_ANY, 'Port:')
		self.proxyPort = wx.TextCtrl(self.networkSettingsPanel, wx.ID_ANY)
		self.proxyPort.SetValue(str(Config.settings.proxyPort))
		self.proxyPortSizer.Add(self.proxyPortLbl, 0, wx.EXPAND)
		self.proxyPortSizer.Add(self.proxyPort, 0, wx.EXPAND)		
		
		self.proxySettingsSizer = wx.BoxSizer(wx.HORIZONTAL)	
		self.proxySettingsSizer.Add(self.proxyTypeSizer, 2, wx.EXPAND, PADDING)
		#self.proxySettingsSizer.Add(self.proxyAddrSizer, 2, wx.EXPAND, PADDING)
		self.proxySettingsSizer.Add(self.proxyPortSizer, 1, wx.EXPAND, PADDING)
		
		
		self.proxyBoxSizer.Add(self.useProxy, 0, wx.EXPAND)
		self.proxyBoxSizer.Add(self.proxyAddrSizer, 0, wx.EXPAND)
		self.proxyBoxSizer.Add(self.proxySettingsSizer, 0, wx.EXPAND)
		
		self.networkSettingsSizer.Add(self.proxyBoxSizer, 0, wx.EXPAND)			
		
		
		self.networkSettingsPanel.SetSizerAndFit(self.networkSettingsSizer)		
		self.networkSettingsPanel.SetAutoLayout(True)
		self.networkSettingsPanel.Layout()
		
		

		self.noteBook.AddPage(self.generalSettingsPanel, 'General Settings')		
		self.noteBook.AddPage(self.networkSettingsPanel, 'Netork Settings')		



		self.buttonsPanel = wx.Panel(self.splitter, wx.ID_ANY)
		self.buttonsPanelSizer = wx.BoxSizer(wx.VERTICAL)
		self.okBut = wx.Button(self.buttonsPanel, ID_OK_BUT, 'Save')
		wx.EVT_BUTTON(self, ID_OK_BUT, self.OnClickSave)
		self.closeBut = wx.Button(self.buttonsPanel, ID_CLOSE_BUT, 'Close')
		wx.EVT_BUTTON(self, ID_CLOSE_BUT, self.OnClickClose)
		self.buttonsSizer = wx.BoxSizer(wx.HORIZONTAL)
		self.buttonsSizer.Add(self.okBut, 0, wx.CENTER)
		self.buttonsSizer.Add(self.closeBut, 0, wx.CENTER)		
		self.buttonsPanelSizer.Add(self.buttonsSizer, 0, wx.ALIGN_CENTER | wx.ALIGN_BOTTOM)
		self.buttonsPanel.SetSizerAndFit(self.buttonsPanelSizer)
		

		self.splitter.SplitHorizontally(self.noteBookPanel, self.buttonsPanel)		
		self.splitterSizer = wx.BoxSizer(wx.VERTICAL)		
		self.splitterSizer.Add(self.splitter, 1, wx.EXPAND)	
		self.SetSizer(self.splitterSizer)		
		
	
		self.mainSizer.Add(self.noteBook, 0, wx.EXPAND)
		self.noteBookPanel.SetSizerAndFit(self.mainSizer)		
		#self.noteBookPanel.SetAutoLayout(True)
		#self.noteBookPanel.Layout()
		
		self.Center(wx.BOTH)
		self.Fit()
		self.Show(True)
		
		
	def onSelectIncomingDir(self, event):		
		if (self.incomingDirDialog):
			self.incomingDirDialog.show()
		else:
			self.incomingDirDialog = wx.DirDialog(self, 'Please select a directory for your incoming files', Config.settings.downloadDir)
			if self.incomingDirDialog.ShowModal() == wx.ID_OK:
				self.incomingDirName = self.incomingDirDialog.GetPath()
				if (Config.checkExistence(self.incomingDirName, TYPE_DIR) != EXIST_W):
					self.incomingDirMessageDialog = wx.MessageDialog(self, 'You dont have permission to write to this directory', 'Error', style = wx.OK)
					self.incomingDirMessageDialog.ShowModal()
				else:
					Config.settings.downloadDir = self.incomingDirName
					self.incomingDir.SetValue(Config.settings.downloadDir)
				
			self.incomingDirDialog.Destroy()
		
		
	def onSelectTmpDir(self, event):		
		if (self.tmpDirDialog):
			self.tmpDirDialog.show()
		else:
			self.tmpDirDialog = wx.DirDialog(self, 'Please select a directory for temporary files', Config.settings.tmpDir)
			if self.tmpDirDialog.ShowModal() == wx.ID_OK:
				self.tmpDirName = self.tmpDirDialog.GetPath()
				if (Config.checkExistence(self.tmpDirName, TYPE_DIR) != EXIST_W):
					self.tmpDirMessageDialog = wx.MessageDialog(self, 'You dont have permission to write to this directory', 'Error', style = wx.OK)
					self.tmpDirMessageDialog.ShowModal()
				else:
					Config.settings.tmpDir = self.tmpDirName
					self.tmpDir.SetValue(Config.settings.tmpDir)
				
			self.tmpDirDialog.Destroy()	
		
		
		

	def OnClickSave(self, event):
		Config.settings.rapidshareUsername = self.username.GetValue()
		Config.settings.rapidsharePassword = self.password.GetValue()
		Config.settings.downloadDir = self.incomingDir.GetValue()
		Config.settings.tmpDir = self.tmpDir.GetValue()
		Config.settings.maxConnectionPerFile = int(self.numberOfConnPerFile.GetValue())
		Config.settings.maxConcurrentDownload = int(self.numberOfConn.GetValue())
		Config.settings.maxRetry = int(self.maxRetry.GetValue())
		Config.settings.useProxy = self.useProxy.GetValue()
		Config.settings.proxyType = proxyTypeCurlList[self.proxyTypeList.GetValue()]
		Config.settings.proxyAddr = str(self.proxyAddr.GetValue())
		Config.settings.proxyPort = int(self.proxyPort.GetValue())
		
		Config.save()
		self.Destroy()
		
	def OnClickClose(self, event):
		self.Destroy()