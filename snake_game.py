import tkinter
import random

ROWS = 25
COLS = 25
TILE_SIZE = 25

WINDOW_WIDTH = TILE_SIZE * COLS
WINDOW_HEIGHT = TILE_SIZE * ROWS

class Tile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

#create the game window
window = tkinter.Tk()
window.title('Snake Game')
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "gray", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

#place the window in the center
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

#format "(w)x(h)+(x)+(y)"
window.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')

#initialize the game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) #single tile, snake's head

def draw():
    global snake

    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "pink")

    window.after(100, draw) #call draw again every 100ms (1/10 of a second) = 10 frames/second

draw()

window.mainloop()
