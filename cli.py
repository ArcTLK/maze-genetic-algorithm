import sys
import wx
from maze_gui import GridPanelFrame

if __name__ == '__main__':
    moves = sys.argv[1]

    app = wx.App()
    frame = GridPanelFrame(None)
    
    for i in range(len(moves)):
        if moves[i] == '0':
            moves[i] = 'N'
        elif moves[i] == '1':
            moves[i] = 'W'
        elif moves[i] == '2':
            moves[i] = 'S'
        elif moves[i] == '3':
            moves[i] = 'A'
        elif moves[i] == '4':
            moves[i] = 'D'
            
    frame.PlayGame([move for move in list(moves) if move != 'N'])
    
    app.MainLoop()

   