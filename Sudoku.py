import random
import tkinter as tk
from tkinter import messagebox


class Sudoku(tk.Frame):
    def __init__(self, parent):
        """ Constructor for Sudoku """
        super().__init__(parent)
        self.parent = parent
        self.gameGrid = [[tk.Entry for a in range(9)] for _ in range(9)]

        # Create a Frame to hold the grid and the button
        grid_frame = tk.Frame(self)
        grid_frame.pack(side="top", fill="both", expand=True)

        for i in range(9):
            for j in range(9):
                self.gameGrid[i][j] = tk.Entry(grid_frame, width=2, font=('Courier', 40), justify='center',
                                               validate="key",
                                               validatecommand=(self.register(self.on_validate), '%P', str(i), str(j)))
                self.gameGrid[i][j].grid(row=i, column=j, sticky="nsew")
                if i % 3 == 0:  # Add thicker top border on new 3x3 blocks
                    self.gameGrid[i][j].grid(pady=(5, 1))
                if j % 3 == 0:  # Add thicker left border on new 3x3 blocks
                    self.gameGrid[i][j].grid(padx=(5, 1))

        # Button to check the solution
        self.check_button = tk.Button(self, text="Check Answer", command=self.check_answer)
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
