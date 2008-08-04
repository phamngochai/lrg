import wx
import wx.grid

from Const import *
from decimal import *


BG_QUEUEING = wx.Color(255, 255, 255)
BG_DOWNLOADING = wx.Color(204, 230, 255)
BG_DONE = wx.Color(153, 204, 255)
BG_COMPLETING = wx.Color(204, 255, 153)
BG_STOPPED = wx.Color(255, 255, 204)
BG_EXIST = wx.Color(0, 214, 71)
BG_ERROR = wx.Color(235, 78, 0)

colorList = {}
colorList[STAT_Q] = BG_QUEUEING
colorList[STAT_D] = BG_DOWNLOADING
colorList[STAT_C] = BG_COMPLETING
colorList[STAT_S] = BG_STOPPED
colorList[STAT_Z] = BG_DONE
colorList[STAT_X] = BG_EXIST
colorList[STAT_E] = BG_ERROR



class DownloadFileGrid(wx.grid.Grid):
	def __init__(self, parent, id, panelPos, popupMenuCallback = None):
		wx.grid.Grid.__init__(self, parent, wx.ID_ANY)
		self.panelPos = panelPos
		self.popupMenuCallback = popupMenuCallback	
		self.CreateGrid(0, 9)
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
		#self.SetColLabelValue(ID_COL, "Id")
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
		self.SetColSize(FILEURL_COL, FILEURL_COL_SIZE)
		self.SetColSize(FILEERROR_COL, FILEERROR_COL_SIZE)
		
		self.SetColAttr(FILESPEED_COL, self.alignRight)
		self.SetColAttr(FILESTATUS_COL, self.alignRight)
		self.SetColAttr(FILESIZE_COL, self.alignRight)
		self.SetColAttr(PERCENT_COL, self.alignRight)
		self.SetColAttr(RETRY_COL, self.alignRight)
		self.SetColAttr(FILECOMP_COL, self.alignRight)
		
		
		self.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.onSelectedURLs)
		
	#def update(self, downloadFile):
		#wx.CallAfter(self.realUpdate, downloadFile)

	def getAllSelectedURLS(self):
		selectedURLS = []
		topLeft = self.GetSelectionBlockTopLeft()
		botRight = self.GetSelectionBlockBottomRight()
		#print '--------'
		#print topLeft
		#print botRight
		
		for i in range(len(topLeft)):
			for j in range(topLeft[i][0], botRight[i][0] + 1):
				selectedURLS.append(str(self.GetCellValue(j, FILEURL_COL)))
				
		return selectedURLS
		
		
	def onSelectedURLs(self, event):
		#print event.GetPosition()
		selectedURLS = self.getAllSelectedURLS()
		if (len(selectedURLS) > 0):
			self.popupMenuCallback(selectedURLS, event.GetPosition(), self.panelPos)
	
		
	def update(self, downloadFile, updateType):
		#print 'UPDATE CALL', downloadFile
		
		for i in range(0, self.GetNumberRows()):
			if (self.GetCellValue(i, FILEURL_COL) == downloadFile.getFileURL()):
				if (updateType != None):
					for col in updateType:
						self.SetCellValue(i, col, downloadFile.getInfoByCol(col))
						if (col == FILESTATUS_COL):
							tmpAttr = wx.grid.GridCellAttr()
							tmpAttr.SetBackgroundColour(colorList[downloadFile.getStatus()])
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
		self.SetCellValue(nbRow, FILENAME_COL, downloadFile.getInfoByCol(FILENAME_COL))
		self.SetCellValue(nbRow, FILESTATUS_COL, downloadFile.getInfoByCol(FILESTATUS_COL))
		self.SetCellValue(nbRow, FILESIZE_COL, downloadFile.getInfoByCol(FILESIZE_COL))
		self.SetCellValue(nbRow, FILECOMP_COL, downloadFile.getInfoByCol(FILECOMP_COL))
		self.SetCellValue(nbRow, PERCENT_COL, downloadFile.getInfoByCol(PERCENT_COL))
		self.SetCellValue(nbRow, RETRY_COL, downloadFile.getInfoByCol(RETRY_COL))
		self.SetCellValue(nbRow, FILEURL_COL, downloadFile.getInfoByCol(FILEURL_COL))
		tmpAttr = wx.grid.GridCellAttr()
		tmpAttr.SetBackgroundColour(colorList[downloadFile.getStatus()])
		#print 'Color ', colorList[downloadFile.getStatus()]
		
		self.SetRowAttr(nbRow, tmpAttr)

		self.ForceRefresh()
		
	def removeDownloadFile(self, downloadFile):
		for i in range(0, self.GetNumberRows()):
			if (self.GetCellValue(i, FILEURL_COL) == downloadFile.getFileURL()): 
				self.DeleteRows(i)
				break
		self.ForceRefresh()
		
	def removeDownloadFileURL(self, fileURL):
		for i in range(0, self.GetNumberRows()):
			if (self.GetCellValue(i, FILEURL_COL) == fileURL):
				self.DeleteRows(i)
				break
		self.ForceRefresh()
		
		
	def removeAllDownloadFile(self):
		if (self.GetNumberRows() != 0):
			self.DeleteRows(0, self.GetNumberRows())