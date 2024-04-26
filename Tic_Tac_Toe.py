import tkinter as tk
import tkinter.messagebox as messagebox


class TicTacToe(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.current_player = 'X'  # Start game with player X
        self.buttons = [[tk.Button for a in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j] = tk.Button(self, text=' ', font=('Arial', 47), height=2, width=5,
                                               command=lambda i=i, j=j: self.on_button_click(i, j), bg='white',
                                               fg='black')
                self.buttons[i][j].grid(row=i, column=j, sticky="nsew")

    def on_button_click(self, i, j):
        if self.buttons[i][j]['text'] == ' ' and not self.check_winner():
            self.buttons[i][j]['text'] = self.current_player
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
            if self.buttons[i][0]['text'] == self.buttons[i][1]['text'] == self.buttons[i][2]['text'] != ' ':
                for j in range(3):
                    self.buttons[i][j].config(bg='green')
                return True
            if self.buttons[0][i]['text'] == self.buttons[1][i]['text'] == self.buttons[2][i]['text'] != ' ':
                for j in range(3):
                    self.buttons[j][i].config(bg='green')
                return True
        # Check diagonals
        if self.buttons[0][0]['text'] == self.buttons[1][1]['text'] == self.buttons[2][2]['text'] != ' ':
            for j in range(3):
                self.buttons[j][j].config(bg='green')
            return True
        if self.buttons[0][2]['text'] == self.buttons[1][1]['text'] == self.buttons[2][0]['text'] != ' ':
            self.buttons[0][2].config(bg='green')
            self.buttons[1][1].config(bg='green')
            self.buttons[2][0].config(bg='green')
            return True
        return False

    def check_draw(self):
        # Check if all cells are filled and no winner yet
        return all(self.buttons[i][j]['text'] != ' ' for i in range(3) for j in range(3))

    def reset_game(self):
        # Reset the game by clearing all buttons and setting start player
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text=' ')
                self.buttons[i][j].config(bg='white')
        self.current_player = 'X'  # X starts the new game


