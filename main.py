import tkinter as tk
from Sudoku import Sudoku
from Tic_Tac_Toe import TicTacToe

class MainFrame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Game Collection')

        # Main container for games
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Buttons container
        button_frame = tk.Frame(self)
        button_frame.pack(side="top", fill="x")

        self.frames = {}
        for GameClass in (Sudoku, TicTacToe):
            frame = GameClass(container)
            self.frames[GameClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

            # Button for each game
            button = tk.Button(button_frame, text=GameClass.__name__,
                               command=lambda name=GameClass.__name__: self.show_frame(name))
            button.pack(side="left")

        self.show_frame("Sudoku")  # Default show Sudoku

    def show_frame(self, name):
        """Bring the selected game frame to the top for display."""
        frame = self.frames[name]
        frame.tkraise()

if __name__ == "__main__":
    app = MainFrame()
    app.mainloop()
