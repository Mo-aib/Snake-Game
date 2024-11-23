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

#game window
window = tkinter.Tk()
window.title("Snake")
window.resizable(False, False)

canvas = tkinter.Canvas(window, bg = "black", width=WINDOW_WIDTH, height=WINDOW_HEIGHT, borderwidth = 0, highlightthickness = 0)
canvas.pack()
window.update()

#center the window
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width/2) - (window_width/2))
window_y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

#initialize game
snake = Tile(5*TILE_SIZE, 5*TILE_SIZE) #A single tile for the snakes head
food = Tile(10*TILE_SIZE, 10*TILE_SIZE)
snake_body = [] #multiple snake tiles
VelocityX = 0
VelocityY = 0
gameOver = False
score = 0

def restart_game():
    global snake, food, snake_body, gameOver, score, VelocityX, VelocityY
    snake = Tile(5*TILE_SIZE, 5*TILE_SIZE)#RESET SNAKE POSITION
    food = Tile(random.randint(0, COLS-1) * TILE_SIZE, random.randint(0, ROWS-1) * TILE_SIZE)
    snake_body = []
    VelocityX = 0
    VelocityY = 0
    gameOver = False
    score = 0

def change_direction(e): #e=event
    global snake, food, snake_body, gameOver, score, VelocityX, VelocityY
    if (gameOver):
        if e.keysym == "space":
            restart_game()
        return
    
    if (e.keysym == "Up" and VelocityY != 1):
        VelocityX = 0
        VelocityY = -1
    elif (e.keysym == "Down" and VelocityY !=-1):
        VelocityX = 0
        VelocityY = 1
    elif (e.keysym == "Left" and VelocityX != 1):
        VelocityX = -1
        VelocityY = 0
    elif (e.keysym == "Right" and VelocityX !=-1):
        VelocityX = 1
        VelocityY = 0

    
   
def move():
    global snake, food, snake_body, gameOver, score, VelocityX, VelocityY
    if (gameOver):
        return
    
    if (snake.x < 0 or snake.x > WINDOW_WIDTH - TILE_SIZE or snake.y < 0 or snake.y > WINDOW_HEIGHT - TILE_SIZE):
        gameOver = True
        return
    
    for tile in snake_body:
        if (snake.x == tile.x and snake.y == tile.y):
            gameOver = True
            return
    
    #collision
    if (snake.x == food.x and snake.y == food.y):
        snake_body.append(Tile(food.x,food.y))
        food.x = random.randint(0, COLS-1) * TILE_SIZE
        food.y = random.randint(0, ROWS-1) * TILE_SIZE
        score +=1
        
    #update snakes body
    for i in range (len(snake_body)-1, 0, -1):
        snake_body[i].x = snake_body[i - 1].x
        snake_body[i].y = snake_body[i - 1].y
        
    if len(snake_body) > 0:
        snake_body[0].x = snake.x
        snake_body[0].y = snake.y
    
    
    snake.x += VelocityX * TILE_SIZE
    snake.y += VelocityY * TILE_SIZE
    

def draw():
    global snake, food, snake_body, score
    move()
    
    canvas.delete("all")
    #draw food
    canvas.create_rectangle(food.x, food.y, food.x + TILE_SIZE, food.y + TILE_SIZE, fill = "red")
    
    #draw snake
    canvas.create_rectangle(snake.x, snake.y, snake.x + TILE_SIZE, snake.y + TILE_SIZE, fill = "lime green")
    
    for tile in snake_body:
        canvas.create_rectangle(tile.x, tile.y, tile.x + TILE_SIZE, tile.y + TILE_SIZE, fill = "lime green")
    
    if (gameOver):
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, font= "Arial 20", text = f"Game Over: {score}", fill = "white")
        canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 30, font= "Arial 15", text = f"Press Sapce Bar to restart", fill = "white")
    else:
        canvas.create_text(30, 20, font = "Arial 10", text= f"Score: {score}", fill= "white")
    
    window.after(100, draw)#100ms = 1/10 ie 10 frames per sec
    
draw()

window.bind("<KeyRelease>", change_direction)

window.mainloop()
