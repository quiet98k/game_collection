import random
import tkinter as tk


class Sudoku:
    def __init__(self, root):
        """ Constructor for Sudoku """
        self.root = root
        self.root.title("Sudoku")
        self.grid = [[tk.Entry for a in range(9)] for _ in range(9)]
        for i in range(9):
            for j in range(9):
                self.grid[i][j] = tk.Entry(root, width=2, font=('Courier', 40), justify='center', validate="key",
                                           validatecommand=(root.register(self.on_validate), '%P', str(i), str(j)))
                self.grid[i][j].grid(row=i, column=j, sticky="nsew")
                if i % 3 == 0:  # Add thicker top border on new 3x3 blocks
                    self.grid[i][j].grid(pady=(5, 1))
                if j % 3 == 0:  # Add thicker left border on new 3x3 blocks
                    self.grid[i][j].grid(padx=(5, 1))
        self.initializeSudoku()

    def remove(self, row, col):
        """ Remove a cell from the Sudoku grid """
        self.grid[row][col].delete(0, tk.END)

    def set(self, row, col, value):
        """ Set value of a certain cell """
        self.remove(row, col)
        self.grid[row][col].insert(tk.END, str(value))

    def get(self, row, col):
        """ Get a value from the grid as String"""
        return self.grid[row][col].get()

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
                    self.grid[row][col].delete(0, tk.END)  # Backtrack by clearing the cell

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
        row, col = int(row), int(col)
        if P == "" or (P.isdigit() and 1 <= int(P) <= 9):
            current_value = P if P.isdigit() else None
            conflicts = self.find_conflicts(row, col, current_value)
            self.reset_highlights()  # Reset before applying new highlights
            if conflicts:
                for conflict in conflicts:
                    self.highlight_error(*conflict)
            return True  # Always return True to allow input
        return False

    def find_conflicts(self, row, col, num):
        conflicts = []
        if num is None:
            return conflicts  # No conflicts if the cell is cleared
        # Check row for duplicates
        if any(self.get(row, j) == str(num) for j in range(9) if j != col):
            conflicts.append(('row', row))
        # Check column for duplicates
        if any(self.get(i, col) == str(num) for i in range(9) if i != row):
            conflicts.append(('col', col))
        # Check 3x3 box for duplicates
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if (self.get(i + start_row, j + start_col) == str(num) and
                        (i + start_row != row or j + start_col != col)):
                    conflicts.append(('box', start_row, start_col))
                    break  # Only need to add the box once
        return conflicts

    def highlight_error(self, section, idx1, idx2=None):
        if section == 'row':
            for j in range(9):
                self.grid[idx1][j].config(bg='red')
        elif section == 'col':
            for i in range(9):
                self.grid[i][idx1].config(bg='red')
        elif section == 'box':
            start_row, start_col = idx1, idx2
            for i in range(3):
                for j in range(3):
                    self.grid[i + start_row][j + start_col].config(bg='red')

    def reset_highlights(self):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].config(bg='white')


root = tk.Tk()
game = Sudoku(root)
root.mainloop()
