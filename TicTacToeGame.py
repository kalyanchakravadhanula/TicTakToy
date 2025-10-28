import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.ai_mode = False  # Toggle for single player

        # Main window setup
        self.window = tk.Tk()
        self.window.title("🎮 Ultimate Tic Tac Toe")
        self.window.geometry("420x530")
        self.window.config(bg="#f0f0f0")

        # Heading label
        self.label = tk.Label(self.window, text="Ultimate Tic Tac Toe",
                              font=("Helvetica", 22, "bold"),
                              bg="#f0f0f0", fg="#222")
        self.label.pack(pady=(10, 5))

        # Turn label
        self.turn_label = tk.Label(self.window, text="Player X's Turn",
                                   font=("Helvetica", 14, "bold"),
                                   bg="#f0f0f0", fg="#007acc")
        self.turn_label.pack(pady=(0, 15))

        # Frame for game buttons
        self.frame = tk.Frame(self.window, bg="#f0f0f0")
        self.frame.pack()

        # Board buttons
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(self.frame, text="", font=("Helvetica", 26, "bold"),
                                width=5, height=2, bg="#ffffff", fg="#333",
                                relief="ridge", bd=3,
                                command=lambda i=i, j=j: self.make_move(i, j))
                btn.grid(row=i, column=j, padx=8, pady=8)
                row.append(btn)
            self.buttons.append(row)

        # Restart and AI buttons
        control_frame = tk.Frame(self.window, bg="#f0f0f0")
        control_frame.pack(pady=15)

        self.restart_btn = tk.Button(control_frame, text="🔁 Restart", font=("Helvetica", 12, "bold"),
                                     bg="#4caf50", fg="white", padx=10, pady=5,
                                     command=self.reset_game)
        self.restart_btn.grid(row=0, column=0, padx=8)

        self.ai_btn = tk.Button(control_frame, text="🤖 Play vs Computer", font=("Helvetica", 12, "bold"),
                                bg="#ff9800", fg="white", padx=10, pady=5,
                                command=self.toggle_ai)
        self.ai_btn.grid(row=0, column=1, padx=8)

        self.window.mainloop()

    # ---- GAME LOGIC ----
    def make_move(self, row, col):
        if self.board[row][col] == "":
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player,
                                          fg="#007acc" if self.current_player == "X" else "#ff4d4d")

            if self.check_winner(self.current_player):
                self.highlight_winner(self.current_player)
                messagebox.showinfo("🏆 Game Over", f"Player {self.current_player} wins!")
                self.reset_game(delay=True)
                return
            elif self.is_board_full():
                messagebox.showinfo("🤝 Game Over", "It's a draw!")
                self.reset_game(delay=True)
                return

            # Switch player
            self.current_player = "O" if self.current_player == "X" else "X"
            self.turn_label.config(text=f"Player {self.current_player}'s Turn",
                                   fg="#007acc" if self.current_player == "X" else "#ff4d4d")

            # AI Move
            if self.ai_mode and self.current_player == "O":
                self.window.after(500, self.ai_move)

    def ai_move(self):
        available = [(i, j) for i in range(3) for j in range(3) if self.board[i][j] == ""]
        if not available: return
        row, col = random.choice(available)
        self.make_move(row, col)

    def check_winner(self, player):
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)): return True
            if all(self.board[j][i] == player for j in range(3)): return True
        if all(self.board[i][i] == player for i in range(3)): return True
        if all(self.board[i][2 - i] == player for i in range(3)): return True
        return False

    def highlight_winner(self, player):
        # Highlight winning line in green
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)):
                for j in range(3):
                    self.buttons[i][j].config(bg="#b2ffb2")
            if all(self.board[j][i] == player for j in range(3)):
                for j in range(3):
                    self.buttons[j][i].config(bg="#b2ffb2")
        if all(self.board[i][i] == player for i in range(3)):
            for i in range(3):
                self.buttons[i][i].config(bg="#b2ffb2")
        if all(self.board[i][2 - i] == player for i in range(3)):
            for i in range(3):
                self.buttons[i][2 - i].config(bg="#b2ffb2")

    def is_board_full(self):
        return all(cell != "" for row in self.board for cell in row)

    def reset_game(self, delay=False):
        def reset_now():
            self.board = [["" for _ in range(3)] for _ in range(3)]
            for row in self.buttons:
                for btn in row:
                    btn.config(text="", bg="#ffffff")
            self.current_player = "X"
            self.turn_label.config(text="Player X's Turn", fg="#007acc")

        if delay:
            self.window.after(1000, reset_now)
        else:
            reset_now()

    def toggle_ai(self):
        self.ai_mode = not self.ai_mode
        if self.ai_mode:
            self.ai_btn.config(text="🧑‍🤝‍🧑 2 Player Mode", bg="#9c27b0")
            messagebox.showinfo("AI Mode", "You are now playing against the Computer!")
        else:
            self.ai_btn.config(text="🤖 Play vs Computer", bg="#ff9800")
            messagebox.showinfo("2 Player Mode", "Now playing with a friend!")

# ✅ Run Game
if __name__ == "__main__":
    TicTacToe()
