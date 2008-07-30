import wx
import wx.grid


class DownloadFileGridCellRenderer(wx.grid.PyGridCellRenderer):
	def __init__(self):
		wx.grid.PyGridCellRenderer.__init__(self)
		
	def Draw(self, grid, attr, dc, rect, row, col, isSelected):
		dc.SetBackgroundMode(wx.SOLID)
		dc.SetBrush(wx.Brush(wx.BLACK, wx.SOLID))
		dc.SetPen(wx.TRANSPARENT_PEN)
		dc.DrawRectangleRect(rect)
		
		dc.SetBackgroundMode(wx.TRANSPARENT)
		//dc.SetFont(attr.GetFont())
		
		value = grid.GetCellValue(row, col)
		cellWidth = grid.GetColSize()
		onePercent = int(cellWidth / 100)
		recWidth = value * onePercent
		
		