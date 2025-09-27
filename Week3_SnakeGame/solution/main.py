import tkinter as tk
import random

GAME_WIDTH = 800
GAME_HEIGHT = 500
SPEED = 100
SPACE_SIZE = 20
BODY_PARTS = 3
SNAKE_COLOR = "#39FF14"   # Neon green
FOOD_COLOR = "#FF073A"    # Neon red-pink
BG_COLOR = "#111111"

# ---------------- GLOBALS ----------------
direction = "down"
score = 0
high_score = 0
game_paused = False
wrap_boundaries = False
game_running = False

class Snake:
    def __init__(self, canvas):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR, outline="#00aa00", width=2, tag="snake"
            )
            self.squares.append(square)

class Food:
    def __init__(self, canvas):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR, outline="#ff4f6d", width=2, tag="food"
        )

def next_turn(snake, food):
    global direction, score, high_score, game_paused, game_running

    if not game_running or game_paused:
        return

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    if wrap_boundaries:
        x %= GAME_WIDTH
        y %= GAME_HEIGHT

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE,
        fill=SNAKE_COLOR, outline="#00aa00", width=2
    )
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        score += 1
        label.config(text=f"Score: {score}   High Score: {high_score}")
        canvas.delete("food")
        food = Food(canvas)
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
    if new_direction == "left" and direction != "right":
        direction = new_direction
    elif new_direction == "right" and direction != "left":
        direction = new_direction
    elif new_direction == "up" and direction != "down":
        direction = new_direction
    elif new_direction == "down" and direction != "up":
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    if not wrap_boundaries:
        if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
            return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True
    return False

def game_over():
    global high_score, score, game_running
    canvas.delete("all")
    game_running = False
    if score > high_score:
        high_score = score
    canvas.create_text(
        GAME_WIDTH/2, GAME_HEIGHT/2,
        text=f"GAME OVER\nScore: {score}\nHigh Score: {high_score}\nPress R to Restart",
        fill="red", font=("Arial Black", 26, "bold"), justify="center"
    )

def restart(event=None):
    start_game()

def pause_game(event=None):
    global game_paused
    if game_running:
        game_paused = not game_paused
        if not game_paused:
            next_turn(snake, food)

def set_difficulty(level):
    global SPEED
    if level == "Easy":
        SPEED = 150
    elif level == "Medium":
        SPEED = 100
    elif level == "Hard":
        SPEED = 50

def toggle_boundaries(event=None):
    global wrap_boundaries
    wrap_boundaries = not wrap_boundaries
    status = "ON (Wrap Around)" if wrap_boundaries else "OFF (Normal)"
    boundary_label.config(text=f"Boundaries: {status}")

# ---------------- START MENU ----------------
def show_menu():
    canvas.delete("all")
    label.config(text="Welcome to Snake Game!", font=("Arial", 16), fg="white", bg="#222")
    boundary_label.config(text="Boundaries: OFF (Normal)", fg="white", bg="#222")
    menu_frame.pack(pady=40)

def start_game():
    global snake, food, direction, score, game_paused, game_running
    menu_frame.pack_forget()
    canvas.delete("all")
    direction = "down"
    score = 0
    game_paused = False
    game_running = True
    label.config(text=f"Score: {score}   High Score: {high_score}", fg="#39FF14", bg="#111")
    snake = Snake(canvas)
    food = Food(canvas)
    next_turn(snake, food)

# ---------------- MAIN ----------------
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)
window.configure(bg="#222")

label = tk.Label(window, text="", font=("Arial", 16), bg="#222", fg="white")
label.pack()

boundary_label = tk.Label(window, text="", font=("Arial", 12), bg="#222", fg="white")
boundary_label.pack()

canvas = tk.Canvas(window, bg=BG_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH, highlightthickness=0)
canvas.pack(pady=10)

window.update()

# Controls
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("r", restart)
window.bind("p", pause_game)
window.bind("b", toggle_boundaries)

# Menu Frame with styling
menu_frame = tk.Frame(window, bg="#222")

title_label = tk.Label(menu_frame, text="🐍 Snake Game 🐍",
                       font=("Arial Black", 28, "bold"),
                       fg="#39FF14", bg="#222")
title_label.pack(pady=15)

def styled_button(text, command, color):
    return tk.Button(menu_frame, text=text, command=command,
                     font=("Arial", 14, "bold"),
                     bg=color, fg="white", activebackground="white",
                     activeforeground=color, width=12, relief="flat")

styled_button("Play", start_game, "#39FF14").pack(pady=8)
difficulty_frame = tk.Frame(menu_frame, bg="#222")
difficulty_frame.pack(pady=10)
styled_button("Easy", lambda: set_difficulty("Easy"), "#1E90FF").pack(in_=difficulty_frame, side="left", padx=5)
styled_button("Medium", lambda: set_difficulty("Medium"), "#FFA500").pack(in_=difficulty_frame, side="left", padx=5)
styled_button("Hard", lambda: set_difficulty("Hard"), "#FF073A").pack(in_=difficulty_frame, side="left", padx=5)

styled_button("Exit", window.destroy, "#555").pack(pady=10)

show_menu()

window.mainloop()