"""
  Author: rupanraj19
  Email: rupanraj2002@gmail.com

  Contributor: Wong Zheng Jie
  Email: wzhengjie99@gmail.com
"""

from tkinter import *
import random

# CONSTANTS
GAME_WIDTH = 800
GAME_HEIGHT = 600
SPEED = 100 # LOWER THE NUMBER FASTER THE GAME
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00" #GREEN
FOOD_COLOR = "#FF0000" #RED
BACKGROUND_COLOR = "#000000" #BLACK

class Snake:
    
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(0, BODY_PARTS):
            self.coordinates.append([0,0])
        
        for x,y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill = SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    
    def __init__(self):
        x = random.randint(0, int((GAME_WIDTH/SPACE_SIZE)-1)) * SPACE_SIZE
        y = random.randint(0, int((GAME_HEIGHT/SPACE_SIZE)-1)) * SPACE_SIZE

        self.coordinates = [x,y]

        # draw the food
        canvas.create_oval(x,y,x+ SPACE_SIZE,y+ SPACE_SIZE, fill=FOOD_COLOR, tag = "food")

def next_turn(snake, food):
    
    x,y = snake.coordinates[0]

    if direction == "up":
        y-= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x,y))

    square = canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE, fill=SNAKE_COLOR, tag = "square")

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        global score, high_score

        score += 1

        if score > high_score:
            high_score = score

        label.config(text = "Score:{} High Score:{}".format(score, high_score))
        
        canvas.delete("food")

        food = Food()

    else:

        del snake.coordinates[-1]

        canvas.delete(snake.squares[-1])

        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:    
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    
    global direction 

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

def check_collisions(snake):
    
    x,y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True
    
    for body_parts in snake.coordinates[1:]:
        if x == body_parts[0] and y == body_parts[1]:
            return True

    return False

def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 - 40, font=("consolas", 70), text="GAME OVER", fill="red", tag="game_over")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2 + 40, font=("consolas", 30), text="Press R to Restart", fill="white", tag="restart_text")
    window.bind('r', lambda event: reset_game())

def reset_game():
    global score, direction, snake, food
    canvas.delete(ALL)
    score = 0
    direction = 'down'
    label.config(text='Score:{} High Score:{}'.format(score, high_score))
    snake = Snake()
    food = Food()
    next_turn(snake, food)

window = Tk()
window.title("Snake game")
window.resizable(False,False)

score = 0
high_score = 0
direction = 'down'

label = Label(window, text='Score:{} High Score:{}'.format(score, high_score), font=('consolas',40))
label.pack()

canvas = Canvas(window, bg= BACKGROUND_COLOR, height = GAME_HEIGHT, width = GAME_WIDTH)
canvas.pack()

window.update()
#TO CENTER THE CANVAS/WINDOW
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

window.geometry(f"{window_width}x{window_height}+{x}+{y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()

next_turn(snake, food)

window.mainloop()
