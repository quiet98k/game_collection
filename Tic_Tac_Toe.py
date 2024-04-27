import tkinter as tk
import tkinter.messagebox as messagebox
import customtkinter as ctk

default_color_1 = "#e8e8e8"
default_color_2 = "#b7b7b7"


class TicTacToe(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.current_player = 'X'  # Start game with player X
        self.configure(fg_color=default_color_1, width=900, height=900)
        self.buttons = [[ctk.CTkButton for a in range(3)] for _ in range(3)]
        grid_frame = ctk.CTkFrame(self)
        grid_frame.pack(side="top", fill="both", expand=True)
        grid_frame.configure(fg_color=default_color_2, width=900, height=900)
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = ctk.CTkButton(grid_frame, text=' ', font=('Courier', 40), height=300, width=300,
                                                   command=lambda i=i, j=j: self.on_button_click(i, j),
                                                   fg_color=default_color_1, border_width=1, border_color="black",
                                                   hover_color=default_color_2, corner_radius=0, text_color="black")
                self.buttons[i][j].grid(row=i, column=j, sticky="nsew")
        # Button to check the solution
        self.check_button = ctk.CTkButton(self, text="Reset Game", command=self.reset_game, fg_color=default_color_1,
                                          border_width=1, border_color="black",
                                          hover_color=default_color_2, corner_radius=5, text_color="black",
                                          width=900, height=50, font=('Courier', 40))
        self.check_button.pack(side="bottom", fill="x")

    def on_button_click(self, i, j):
        if self.buttons[i][j].cget("text") == ' ' and not self.check_winner():
            self.buttons[i][j].configure(text=self.current_player)
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                self.reset_game()
            elif self.check_draw():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.reset_game()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_winner(self):
        # Check for three in a row horizontally, vertically, and diagonally
        for i in range(3):
            if self.buttons[i][0].cget("text") == self.buttons[i][1].cget("text") == self.buttons[i][2].cget(
                    "text") != ' ':
                for j in range(3):
                    self.buttons[i][j].configure(fg_color='#27cf27')
                return True
            if self.buttons[0][i].cget("text") == self.buttons[1][i].cget("text") == self.buttons[2][i].cget(
                    "text") != ' ':
                for j in range(3):
                    self.buttons[j][i].configure(fg_color='#27cf27')
                return True
        # Check diagonals
        if self.buttons[0][0].cget("text") == self.buttons[1][1].cget("text") == self.buttons[2][2].cget("text") != ' ':
            for j in range(3):
                self.buttons[j][j].configure(fg_color='#27cf27')
            return True
        if self.buttons[0][2].cget("text") == self.buttons[1][1].cget("text") == self.buttons[2][0].cget("text") != ' ':
            self.buttons[0][2].configure(fg_color='#27cf27')
            self.buttons[1][1].configure(fg_color='#27cf27')
            self.buttons[2][0].configure(fg_color='#27cf27')
            return True
        return False

    def check_draw(self):
        # Check if all cells are filled and no winner yet
        return all(self.buttons[i][j].cget("text") != ' ' for i in range(3) for j in range(3))

    def reset_game(self):
        # Reset the game by clearing all buttons and setting start player
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].configure(text=' ')
                self.buttons[i][j].configure(fg_color='#f8dddd')
        self.current_player = 'X'  # X starts the new game
