import tkinter as tk
from tkinter import messagebox
import random

ROWS, COLS = 6, 7
CELL_SIZE = 80
PLAYER_COLORS = ["red", "yellow"]

class ConnectFour:
    def __init__(self, root):
        self.root = root
        self.root.title("🎮 Connect Four - Week 4")
        self.root.resizable(False, False)
        self.current_player = 0
        self.vs_computer = False
        self.moves = 0
        self.red_score = 0
        self.yellow_score = 0
        self.board = [["" for _ in range(COLS)] for _ in range(ROWS)]

        # Main background canvas with gradient
        self.bg_canvas = tk.Canvas(root, width=COLS*CELL_SIZE+200, height=ROWS*CELL_SIZE+200, highlightthickness=0)
        self.bg_canvas.pack(fill="both", expand=True)
        self.draw_gradient("#ffe6f0", "#cce6ff")

        # Header section frame
        self.header_frame = tk.Frame(self.bg_canvas, bg="#ffffff", pady=10)
        self.header_window = self.bg_canvas.create_window(0, 0, anchor="nw", window=self.header_frame, width=COLS*CELL_SIZE+200)

        # Title on left
        self.title_label = tk.Label(self.header_frame, text="🎮 Connect Four", font=("Arial Rounded MT Bold", 24), bg="#ffffff", fg="#444")
        self.title_label.grid(row=0, column=0, padx=20, sticky="w")

        # Score & Turn info in center
        self.status_frame = tk.Frame(self.header_frame, bg="#ffffff")
        self.status_frame.grid(row=0, column=1, padx=20)
        self.turn_bar = tk.Label(self.status_frame, text="Red's Turn", font=("Arial", 14, "bold"), fg="red", bg="#ffffff")
        self.turn_bar.pack()
        self.score_label = tk.Label(self.status_frame, text="Score - Red: 0 | Yellow: 0", font=("Arial", 12), bg="#ffffff")
        self.score_label.pack()
        self.move_label = tk.Label(self.status_frame, text="Moves: 0", font=("Arial", 12), bg="#ffffff")
        self.move_label.pack()

        # Canvas for game board
        self.canvas = tk.Canvas(self.bg_canvas, width=COLS*CELL_SIZE, height=ROWS*CELL_SIZE, bg="#f9f9f9",
                                highlightthickness=5, highlightbackground="#ffffff")
        self.board_window = self.bg_canvas.create_window(100, 100, anchor="nw", window=self.canvas)

        # Bottom buttons frame
        self.btn_frame = tk.Frame(self.bg_canvas, bg="#ffe6f0")
        self.btn_window = self.bg_canvas.create_window((COLS*CELL_SIZE)//2+100, ROWS*CELL_SIZE+140, window=self.btn_frame)

        self.restart_btn = tk.Button(self.btn_frame, text="🔄 Restart", command=self.restart_game,
                                     font=("Arial", 12, "bold"), bg="#ffcccc", fg="black", relief="flat", padx=15, pady=5)
        self.restart_btn.grid(row=0, column=0, padx=10)

        self.mode_btn = tk.Button(self.btn_frame, text="👥 PvP Mode", command=self.toggle_mode,
                                  font=("Arial", 12, "bold"), bg="#ccffcc", fg="black", relief="flat", padx=15, pady=5)
        self.mode_btn.grid(row=0, column=1, padx=10)

        # Instructions
        self.instructions = tk.Label(self.bg_canvas,
                                     text="📜 How to Play:\nClick a column to drop your disc.\nGet 4 in a row (horizontal, vertical, diagonal) to win!",
                                     font=("Arial", 12), bg="#ffe6f0", fg="#333")
        self.bg_canvas.create_window((COLS*CELL_SIZE)//2+100, ROWS*CELL_SIZE+200, window=self.instructions)

        # Bind click
        self.canvas.bind("<Button-1>", self.handle_click)

        # Draw initial board
        self.draw_board()

    # Gradient background
    def draw_gradient(self, color1, color2):
        width = COLS*CELL_SIZE+200
        height = ROWS*CELL_SIZE+250
        r1, g1, b1 = self.root.winfo_rgb(color1)
        r2, g2, b2 = self.root.winfo_rgb(color2)
        r_ratio = (r2-r1)/height
        g_ratio = (g2-g1)/height
        b_ratio = (b2-b1)/height
        for i in range(height):
            nr = int(r1 + (r_ratio*i))
            ng = int(g1 + (g_ratio*i))
            nb = int(b1 + (b_ratio*i))
            color = f"#{nr>>8:02x}{ng>>8:02x}{nb>>8:02x}"
            self.bg_canvas.create_line(0, i, width, i, fill=color)

    # Draw discs
    def draw_board(self):
        self.canvas.delete("disc")
        for r in range(ROWS):
            for c in range(COLS):
                x1, y1 = c*CELL_SIZE, r*CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                fill_color = self.board[r][c] if self.board[r][c] else "#e0e0e0"
                self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill=fill_color, outline="#b56576", width=2, tags="disc")

    # Handle click events
    def handle_click(self, event):
        col = event.x // CELL_SIZE
        if col < 0 or col >= COLS: return
        if self.make_move(col):
            self.check_winner()
            if self.vs_computer and self.current_player == 1:
                self.root.after(500, self.computer_move)

    # Place disc
    def make_move(self, col):
        for row in reversed(range(ROWS)):
            if not self.board[row][col]:
                self.board[row][col] = PLAYER_COLORS[self.current_player]
                self.moves += 1
                self.move_label.config(text=f"Moves: {self.moves}")
                self.draw_board()
                self.glow_effect(row, col, PLAYER_COLORS[self.current_player])
                self.current_player = 1 - self.current_player
                self.turn_bar.config(text=f"{'Red' if self.current_player==0 else 'Yellow'}'s Turn",
                                     fg=PLAYER_COLORS[self.current_player])
                return True
        return False

    # Simple AI
    def computer_move(self):
        available_cols = [c for c in range(COLS) if not self.board[0][c]]
        if available_cols:
            col = random.choice(available_cols)
            self.make_move(col)
            self.check_winner()

    # Check win
    def check_winner(self):
        def four_in_a_row(lst):
            return any(lst[i] == lst[i+1] == lst[i+2] == lst[i+3] != "" for i in range(len(lst)-3))
        for r in range(ROWS):
            for c in range(COLS-3):
                if four_in_a_row([self.board[r][c+i] for i in range(4)]):
                    return self.end_game(self.board[r][c])
        for r in range(ROWS-3):
            for c in range(COLS):
                if four_in_a_row([self.board[r+i][c] for i in range(4)]):
                    return self.end_game(self.board[r][c])
        for r in range(ROWS-3):
            for c in range(COLS-3):
                if four_in_a_row([self.board[r+i][c+i] for i in range(4)]):
                    return self.end_game(self.board[r][c])
        for r in range(3, ROWS):
            for c in range(COLS-3):
                if four_in_a_row([self.board[r-i][c+i] for i in range(4)]):
                    return self.end_game(self.board[r][c])
        if all(self.board[0][c] for c in range(COLS)):
            return self.end_game("Draw")

    # End game
    def end_game(self, winner):
        if winner == "Draw":
            messagebox.showinfo("Game Over", "It's a Draw! 🤝")
        else:
            messagebox.showinfo("Game Over", f"{winner.capitalize()} Wins! 🎉")
            if winner == "red":
                self.red_score += 1
            elif winner == "yellow":
                self.yellow_score += 1
        self.score_label.config(text=f"Score - Red: {self.red_score} | Yellow: {self.yellow_score}")
        self.restart_game()

    # Glow effect
    def glow_effect(self, row, col, color):
        x1, y1 = col*CELL_SIZE, row*CELL_SIZE
        x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
        glow = self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill=color, outline="white", width=4)
        self.root.after(300, lambda: self.canvas.delete(glow))

    # Restart game
    def restart_game(self):
        self.board = [["" for _ in range(COLS)] for _ in range(ROWS)]
        self.current_player = 0
        self.moves = 0
        self.move_label.config(text=f"Moves: {self.moves}")
        self.turn_bar.config(text="Red's Turn", fg="red")
        self.draw_board()

    # Toggle PvP / PvC
    def toggle_mode(self):
        self.vs_computer = not self.vs_computer
        mode_text = "🤖 PvC Mode" if self.vs_computer else "👥 PvP Mode"
        self.mode_btn.config(text=mode_text)
        self.restart_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = ConnectFour(root)
    root.mainloop()
