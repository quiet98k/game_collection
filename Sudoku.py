import random
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

default_color_1 = "#e8e8e8"
default_color_2 = "#b7b7b7"
default_color_3 = "#8c8c8c"
default_color_4 = "#525252"


class Sudoku(ctk.CTkFrame):

    def __init__(self, parent):
        """ Constructor for Sudoku """
        super().__init__(parent)
        self.parent = parent
        self.gameGrid = [[None for _ in range(9)] for _ in range(9)]
        self.configure(fg_color='#525252', width=900, height=900)

        # Create a Frame to hold all the 3x3 subgrid frames
        main_grid_frame = ctk.CTkFrame(self, fg_color=default_color_1, border_width=2)
        main_grid_frame.pack(fill="both", expand=True)

        # Creating 9 subgrid frames
        subgrid_frames = [
            [ctk.CTkFrame(main_grid_frame, fg_color=default_color_1, border_width=1, width=300, height=300) for _ in range(3)]
            for _ in range(3)]
        for row in range(3):
            for col in range(3):
                subgrid_frames[row][col].grid(row=row, column=col, padx=1, pady=1, sticky="nsew")

        # Initialize all entries in each subgrid
        for i in range(9):
            for j in range(9):
                subgrid_row, subgrid_col = i // 3, j // 3
                self.gameGrid[i][j] = ctk.CTkEntry(subgrid_frames[subgrid_row][subgrid_col], width=100, height=100,
                                                   font=('Courier', 40),
                                                   justify='center', validate="key", validatecommand=(
                        self.register(self.on_validate), '%P', i, j),
                                                   fg_color="#e8e8e8", border_width=1, border_color="black",
                                                   corner_radius=0, text_color="black")
                self.gameGrid[i][j].grid(row=i % 3, column=j % 3, sticky="nsew")

        # Button to check the solution
        self.check_button = ctk.CTkButton(self, text="Check Answer", command=self.check_answer, fg_color="#e8e8e8",
                                          border_width=1, border_color="black",
                                          hover_color="#b7b7b7", corner_radius=5, text_color="black",
                                          width=900, height=50, font=('Courier', 40))
        self.check_button.pack(side="bottom", fill="x")

        self.initializeSudoku()

    def remove(self, row, col):
        """ Remove a cell from the Sudoku grid """
        self.gameGrid[row][col].delete(0, tk.END)

    def set(self, row, col, value):
        """ Set value of a certain cell """
        self.remove(row, col)
        self.gameGrid[row][col].insert(tk.END, str(value))

    def get(self, row, col):
        """ Get a value from the grid as String"""
        return self.gameGrid[row][col].get()

    def initializeSudoku(self, level=3):
        """initialize the Sudoku board"""

        def init_Internal(row, col):
            if row == 9:  # If the last row is completed, puzzle is complete
                return True
            if col == 9:  # If the last column in the row is reached, move to the next row
                return init_Internal(row + 1, 0)
            if self.get(row, col):  # If current cell is already filled, skip it
                return init_Internal(row, col + 1)

            randNum = list(range(1, 10))
            random.shuffle(randNum)
            for num in randNum:
                if self.is_valid(row, col, num):
                    self.set(row, col, num)
                    if init_Internal(row, col + 1):
                        return True
                    self.gameGrid[row][col].delete(0, tk.END)  # Backtrack by clearing the cell

            return False

        init_Internal(0, 0)
        numToRemove = level * 10
        while numToRemove > 0:
            i, j = random.randint(0, 8), random.randint(0, 8)
            if self.get(i, j) != "":
                self.set(i, j, "")
                numToRemove -= 1
        # disable all the nonempty cell
        for row in range(9):
            for col in range(9):
                if self.get(row, col) != "":
                    self.gameGrid[row][col].configure(state=tk.DISABLED)
                    self.gameGrid[row][col].configure(fg_color="#b7b7b7")
                else:
                    self.gameGrid[row][col].configure(state=tk.NORMAL)

    def is_valid(self, row, col, num):
        """check if num is valid"""
        # check row and column
        for i in range(9):
            if str(num) == self.get(row, i) or str(num) == self.get(i, col):
                return False
        # check boxs
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.get(i + start_row, j + start_col) == str(num):
                    return False
        return True

    def on_validate(self, P, row, col):
        if not (P == "" or (len(P) == 1 and P.isdigit() and 1 <= int(P) <= 9)):
            return False
        # May have more feature here

        return True

    def check_answer(self):
        """ Method to check the Sudoku solution when the button is clicked """
        if self.check_winner():
            messagebox.showinfo("Result", "Congratulations! You solved the puzzle correctly!")
            self.restartGame(3)
        else:
            messagebox.showinfo("Result", "There are mistakes in your solution. Keep trying!")

    def restartGame(self, level):
        for row in range(9):
            for col in range(9):
                self.set(row, col, "")
                self.gameGrid[row][col].configure(state=tk.NORMAL, fg_color="#e8e8e8")
        self.initializeSudoku(level)

    def check_winner(self):
        """ Check if the Sudoku puzzle is correctly solved """

        try:
            for row in range(9):
                if not self.valid_group([self.get(row, col) for col in range(9)]):
                    return False
            for col in range(9):
                if not self.valid_group([self.get(row, col) for row in range(9)]):
                    return False
            for startRow in range(0, 9, 3):
                for startCol in range(0, 9, 3):
                    if not self.valid_group([self.get(row, col)
                                             for row in range(startRow, startRow + 3)
                                             for col in range(startCol, startCol + 3)]):
                        return False
            return True
        except ValueError:
            return False

    def valid_group(self, items):
        """ Helper method to check if a group of 9 cells contains all digits 1-9 exactly once """
        items = [item for item in items if item.isdigit()]
        return len(items) == 9 and len(set(items)) == 9
