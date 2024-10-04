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
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
snake_body = [] #multiple snake tiles
velocityX = 0
velocityY = 0
game_over = False
score = 0

#game loop
def change_direction(event):
    #print(event)
    #print(event.keysym)

    global velocityX, velocityY, game_over
    if (game_over):
        return

    if (event.keysym == "Up" and velocityY != 1):
        velocityX = 0
        velocityY = -1

    elif (event.keysym == "Down" and velocityY != -1):
        velocityX = 0
        velocityY = 1
    
    elif (event.keysym == "Left" and velocityX != 1):
        velocityX = -1
        velocityY = 0

    elif (event.keysym == "Right" and velocityX != -1):
        velocityX = 1
        velocityY = 0


def move():
    global snake, food, snake_body, game_over, score
    if (game_over):
        return
    
    if (snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT):
        game_over = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            game_over = True
            return

    #collision
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x, food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score += 1

    #update the snake body
    for viper in range(len(snake_body)-1, -1, -1):
        tile = snake_body[viper]
        if (viper == 0):
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[viper-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE


def draw():
    global snake, food, snake_body, game_over, score
    move()

    canvas.delete("all")

    #draw the food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "yellow")

    #draw the snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "pink")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "pink")

    if (game_over):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font = "Helvetica 20", text = f"Game Over: {score}", fill = "red")
    else:
        canvas.create_text(30, 20, font = "Helvetica 10", text = f"Score: {score}", fill = "white")

    window.after(100, draw) #call draw again every 100ms (1/10 of a second) = 10 frames/second

draw()
window.bind("<KeyRelease>", change_direction)
window.mainloop()