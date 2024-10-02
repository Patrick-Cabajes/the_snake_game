import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

#create the game window
window = tkinter.Tk()
window.title('Snake Game')
window.resizable(False, False)

window.mainloop()
