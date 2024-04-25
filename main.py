import tkinter as tk

from Tic_Tac_Toe import TicTacToe
from Sudoku import Sudoku


def main():
    root = tk.Tk()
    root.title("Tic Tac Toe Game")
    game1 = TicTacToe(root)
    game1.pack()  # Add some padding around the frame for aesthetics
    game2 = Sudoku(root)
    game2.pack()

    root.mainloop()


if __name__ == "__main__":
    main()
