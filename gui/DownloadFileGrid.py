import wx
import wx.grid

from Const import *
from decimal import *


COLOR_QUEUEING = wx.Color(0x00, 0x00, 0x00)
COLOR_DOWNLOADING = wx.Color(0x00, 0x00, 0xFF)
COLOR_DONE = wx.Color(0x00, 0x80, 0x00)
COLOR_COMPLETING = wx.Color(0x00, 0xCC, 0x00)
COLOR_STOPPED = wx.Color(0x99, 0x99, 0x00)
COLOR_EXIST = wx.Color(0xFF, 0x33, 0xCC)
COLOR_ERROR = wx.Color(0xFF, 0x00, 0x00)

colorList = {}
colorList[STAT_Q] = COLOR_QUEUEING
colorList[STAT_D] = COLOR_DOWNLOADING
colorList[STAT_C] = COLOR_COMPLETING
colorList[STAT_S] = COLOR_STOPPED
colorList[STAT_Z] = COLOR_DONE
colorList[STAT_X] = COLOR_EXIST
colorList[STAT_E] = COLOR_ERROR



class DownloadFileGrid(wx.grid.Grid):
	def __init__(self, parent, id, panelPos, popupMenuCallback = None, keyPressedCallback = None):
		wx.grid.Grid.__init__(self, parent, wx.ID_ANY)
		self.panelPos = panelPos
		self.popupMenuCallback = popupMenuCallback
		self.keyPressedCallback = keyPressedCallback	
		self.CreateGrid(0, 10)
		self.SetCellHighlightPenWidth(0)
		self.SetSelectionMode(wx.grid.Grid.SelectRows)
		self.DisableDragRowSize()
		self.SetRowLabelSize(0)
		self.EnableGridLines(False)
		self.EnableEditing(False)
		self.SetDefaultCellOverflow(False)
		self.SetDefaultCellAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTRE)
		self.alignRight = wx.grid.GridCellAttr()
		self.alignRight.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTRE)
		
		self.SetColMinimalAcceptableWidth(0)
		self.SetColMinimalWidth(FILEID_COL, 0)
		self.AutoSizeColumn(FILEID_COL, False)
		self.SetColSize(FILEID_COL, 0)		
		
		self.SetColLabelValue(FILEID_COL, "")
		self.SetColLabelValue(FILENAME_COL, "File name")
		self.SetColLabelValue(FILESPEED_COL, "Speed")
		self.SetColLabelValue(FILESTATUS_COL, "Status")
		self.SetColLabelValue(FILESIZE_COL, "File size")
		self.SetColLabelValue(FILECOMP_COL, "Completed")
		self.SetColLabelValue(PERCENT_COL, "Percent")
		self.SetColLabelValue(RETRY_COL, "Retry")
		self.SetColLabelValue(FILEURL_COL, "Address")
		self.SetColLabelValue(FILEERROR_COL, "Error")

		self.SetColSize(FILENAME_COL, FILENAME_COL_SIZE)
		self.SetColSize(FILESTATUS_COL, FILESTATUS_COL_SIZE)
		self.SetColSize(FILESPEED_COL, FILESPEED_COL_SIZE)
		self.SetColSize(FILECOMP_COL, FILECOMP_COL_SIZE)
		self.SetColSize(FILEURL_COL, FILEURL_COL_SIZE)
		self.SetColSize(FILEERROR_COL, FILEERROR_COL_SIZE)
		
		self.SetColAttr(FILESPEED_COL, self.alignRight)
		self.SetColAttr(FILESTATUS_COL, self.alignRight)
		self.SetColAttr(FILESIZE_COL, self.alignRight)
		self.SetColAttr(PERCENT_COL, self.alignRight)
		self.SetColAttr(RETRY_COL, self.alignRight)
		self.SetColAttr(FILECOMP_COL, self.alignRight)
		
		
		self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.onSelectedIds)
		self.Bind(wx.EVT_KEY_UP, self.onKeyPressed)
		
	#def update(self, downloadFile):
		#wx.CallAfter(self.realUpdate, downloadFile)

	def getAllSelectedIds(self):
		selectedIds = []
		topLeft = self.GetSelectionBlockTopLeft()
		botRight = self.GetSelectionBlockBottomRight()
		#print '--------'
		#print topLeft
		#print botRight		
		for i in range(len(topLeft)):
			for j in range(topLeft[i][0], botRight[i][0] + 1):
				selectedIds.append(int(str(self.GetCellValue(j, FILEID_COL))))				
		
		return selectedIds
		
		
	def onSelectedIds(self, event):
		#print event.GetPosition()
		selectedIds = self.getAllSelectedIds()
		if (len(selectedIds) > 0):
			self.popupMenuCallback(selectedIds, event.GetPosition(), self.panelPos)
			
	def onKeyPressed(self, event):
		#print event.GetKeyCode()
		if event.GetKeyCode() == 127:
			self.keyPressedCallback(self.getAllSelectedIds(), self.panelPos)
			#self.deleteDownloadFile(id)
		elif event.GetKeyCode() == 65 and event.ControlDown():					
			self.SelectAll()
	
		
	def update(self, downloadFile, updateType):
		#print 'UPDATE CALL', downloadFile
		
		for i in range(0, self.GetNumberRows()):
			if (self.GetCellValue(i, FILEID_COL) == downloadFile.getInfoByCol(FILEID_COL)):
				self.SetCellValue(i, PERCENT_COL, downloadFile.getInfoByCol(PERCENT_COL))
				if (updateType != None):
					for col in updateType:
						self.SetCellValue(i, col, downloadFile.getInfoByCol(col))						
						if (col == FILESTATUS_COL):
							tmpAttr = wx.grid.GridCellAttr()
							#tmpAttr.SetBackgroundColour(colorList[downloadFile.getStatus()])
							tmpAttr.SetTextColour(colorList[downloadFile.getStatus()])
							#print 'Color ', colorList[downloadFile.getStatus()]
							self.SetRowAttr(i, tmpAttr)							
						
				break
					
		self.ForceRefresh()
		
		
	#def addDownloadFile(self, downloadFile):
		#wx.CallAfter(self.realAddDownloadFile, downloadFile)
	
	def addDownloadFile(self, downloadFile):
		nbRow = self.GetNumberRows()
		self.InsertRows(nbRow)
		#print 'nbRow', nbRow
		self.SetCellValue(nbRow, FILEID_COL, downloadFile.getInfoByCol(FILEID_COL))
		self.SetCellValue(nbRow, FILENAME_COL, downloadFile.getInfoByCol(FILENAME_COL))
		self.SetCellValue(nbRow, FILESTATUS_COL, downloadFile.getInfoByCol(FILESTATUS_COL))
		self.SetCellValue(nbRow, FILESIZE_COL, downloadFile.getInfoByCol(FILESIZE_COL))
		self.SetCellValue(nbRow, FILECOMP_COL, downloadFile.getInfoByCol(FILECOMP_COL))
		self.SetCellValue(nbRow, PERCENT_COL, downloadFile.getInfoByCol(PERCENT_COL))
		self.SetCellValue(nbRow, RETRY_COL, downloadFile.getInfoByCol(RETRY_COL))
		self.SetCellValue(nbRow, FILEURL_COL, downloadFile.getInfoByCol(FILEURL_COL))
		tmpAttr = wx.grid.GridCellAttr()
		#tmpAttr.SetBackgroundColour(colorList[downloadFile.getStatus()])
		tmpAttr.SetTextColour(colorList[downloadFile.getStatus()])
		#print 'Color ', colorList[downloadFile.getStatus()]
		
		self.SetRowAttr(nbRow, tmpAttr)

		self.ForceRefresh()
		
	def deleteDownloadFile(self, id):
		#print 'downloadFilegrid, deleteDownloadFile'
		for i in range(0, self.GetNumberRows()):
			if (self.GetCellValue(i, FILEID_COL) == str(id)): 
				 
				self.DeleteRows(i)
				break
		self.ForceRefresh()
		
	def removeDownloadFileId(self, fileId):
		for i in range(0, self.GetNumberRows()):
			if (self.GetCellValue(i, FILEID_COL) == fileId):
				self.DeleteRows(i)
				break
		self.ForceRefresh()
		
		
	def removeAllDownloadFile(self):
		if (self.GetNumberRows() != 0):
			self.DeleteRows(0, self.GetNumberRows())