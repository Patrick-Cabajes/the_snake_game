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

# create the game window
window = tkinter.Tk()
window.title('Snake Game')
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "gray", width = WINDOW_WIDTH, height = WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

# place the window in the center
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

# format "(w)x(h)+(x)+(y)"
window.geometry(f'{window_width}x{window_height}+{window_x}+{window_y}')

# initialize the game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) #single tile, snake's head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
snake_body = [] #multiple snake tiles
velocityX = 0
velocityY = 0
next_velocityX = 0
next_velocityY = 0
game_over = False
score = 0
high_score = 0
paused = False
first_start = True
difficulty_selected = False
game_speed = 130

# difficulty levels
difficulty = {
    "Easy": 200,
    "Medium": 130,
    "Hard": 90
}

selected_difficulty = "Medium"

def select_difficulty(event):
    global game_speed, difficulty_selected, selected_difficulty

    if event.char == "1":
        selected_difficulty = "Easy"
    
    elif event.char == "2":
        selected_difficulty = "Medium"

    elif event.char == "3":
        selected_difficulty = "Hard"
    else:
        return #Ignore other keys
    
    game_speed = difficulty[selected_difficulty]
    difficulty_selected = True
    draw() 

# game loop
def change_direction(event):
    global next_velocityX, next_velocityY, velocityX, velocityY, first_start, game_over

    if game_over:
        return
    
    if first_start:
        first_start = False

    if event.keysym == "Up" and velocityY == 0:
        velocityX, velocityY = 0, -1
        next_velocityX, next_velocityY = 0, -1

    elif event.keysym == "Down" and velocityY == 0:
        velocityX, velocityY = 0, 1
        next_velocityX, next_velocityY = 0, 1
    
    elif event.keysym == "Left" and velocityX == 0:
        velocityX, velocityY = -1, 0
        next_velocityX, next_velocityY = -1, 0

    elif event.keysym == "Right" and velocityX == 0:
        velocityX, velocityY = 1, 0
        next_velocityX, next_velocityY = 1, 0

def toggle_pause(event):
    global paused, game_over
    if not game_over:
        paused = not paused

def restart_game(event):
    global snake, food, snake_body, velocityX, velocityY, next_velocityX, next_velocityY, game_over, score, paused, high_score, first_start, difficulty_selected

    if not game_over:
        return

    snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) 
    food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
    snake_body = []
    velocityX = 0
    velocityY = 0
    next_velocityX = 0
    next_velocityY = 0
    game_over = False
    score = 0
    paused = False
    first_start = False
    difficulty_selected = False
    canvas.delete("all")
    draw()

def move():
    global snake, food, snake_body, game_over, score, velocityX, velocityY, next_velocityX, next_velocityY, difficulty_selected

    if game_over or not difficulty_selected:
        return
    
    if not (next_velocityX == -velocityX and next_velocityY == -velocityY):
        velocityX, velocityY = next_velocityX, next_velocityY
    
    # wall collision
    if snake.x < 0 or snake.x >= WINDOW_WIDTH or snake.y < 0 or snake.y >= WINDOW_HEIGHT:
        game_over = True
        return
    
    # snake's collision with itself
    for tile in snake_body:
        if snake.x == tile.x and snake.y == tile.y:
            game_over = True
            return
        
    # snake's food and increase in size
    if snake.x == food.x and snake.y == food.y:
        if snake_body:
            last_tile = snake_body[-1]
            snake_body.append(Tile(last_tile.x, last_tile.y))
        
        else:
            snake_body.append(Tile(snake.x, snake.y))

        score += 1

        while True:
            new_x = random.randint(0, COLS-1) * TILE_SIZE
            new_y = random.randint(0, ROWS-1) * TILE_SIZE

            overlap = any(tile.x == new_x and tile.y == new_y for tile in snake_body)
            if not overlap and (new_x != snake.x or new_y != snake.y):
                food.x = new_x
                food.y = new_y
                break

    # update the snake body
    for viper in range(len(snake_body)-1, -1, -1):
        tile = snake_body[viper]
        if viper == 0:
            tile.x = snake.x
            tile.y = snake.y
        else:
            prev_tile = snake_body[viper-1]
            tile.x = prev_tile.x
            tile.y = prev_tile.y

    snake.x += velocityX * TILE_SIZE
    snake.y += velocityY * TILE_SIZE

def draw():
    global snake, food, snake_body, game_over, score, paused, first_start, difficulty_selected, game_speed

    if not difficulty_selected:
        canvas.delete("all")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 30, font="Helvetica 20 bold", text="Select Difficulty", fill="#FFD700", anchor="center")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font="Helvetica 16", text="1: Easy  |  2: Medium  |  3: Hard", fill="#FFFFFF", anchor="center")
        window.after(100, draw)
        return

    if paused:
        canvas.delete("all")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font = "Helvetica 20 bold", text = "Game Paused", fill = "#F5E1DA")
        window.after(100, draw)
        return

    #prevent automatic start
    if first_start and velocityX == 0 and velocityY == 0 and not game_over:
        canvas.delete("all")
        canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, font = "Helvetica 20 bold", text = "Press Arrow Key to Start", fill = "#FFD700")
        window.after(100, draw)
        return

    move()
    canvas.delete("all")

    #draw the food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "#FFB74D", outline = "black")

    #draw the snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "#D4A373", outline = "black")

    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "#B5651D", outline = "black")

    if game_over:
        global high_score
        if score > high_score:
            high_score = score

        text_x = WINDOW_WIDTH / 2
        text_y = WINDOW_HEIGHT / 2

        canvas.create_text(text_x, text_y - 15, font="Helvetica 20 bold", text=f"Game Over: {score}", fill="#F5E1DA", anchor="center")
        canvas.create_text(text_x, text_y + 15, font="Helvetica 15", text="Press Enter to Restart", fill="#F5E1DA", anchor="center")
        return
    
    else:
        canvas.create_text(45, 20, font = "Helvetica 10 bold", text = f"Score: {score}\nHigh Score: {high_score}", fill = "black")

    window.after(max(game_speed - (score * 1), 80), draw)  

draw()
window.bind("<KeyPress>", change_direction)
window.bind("<space>", toggle_pause)
window.bind("<Return>", restart_game)
window.bind("1", select_difficulty)
window.bind("2", select_difficulty)
window.bind("3", select_difficulty)
window.mainloop()