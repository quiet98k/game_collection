import tkinter as tk
import customtkinter as ctk
from Sudoku import Sudoku
from Tic_Tac_Toe import TicTacToe

default_color_1 = "#e8e8e8"
default_color_2 = "#b7b7b7"
default_color_3 = "#8c8c8c"
default_color_4 = "#525252"

class MainFrame(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Game Collection')
        self.resizable(False, False)
        self.configure(fg_color=default_color_1)

        # Main container for games
        container = ctk.CTkFrame(self)
        container.pack(side="left", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.configure(fg_color=default_color_1)

        # Buttons container
        button_frame = ctk.CTkFrame(self, fg_color=default_color_1)
        button_frame.pack(side="right", fill="y")

        # Dictionary to hold frames for each game
        self.frames = {}
        game_names = []  # List to store game names

        for GameClass in (Sudoku, TicTacToe):
            frame = GameClass(container)
            self.frames[GameClass.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            game_names.append(GameClass.__name__)  # Add game names to the list

        # Combobox to select the game
        self.game_list = ctk.CTkComboBox(button_frame, values=game_names, command=self.change_game, state='readonly',
                                         width=250, height=30, font=('Courier', 30), text_color="black",
                                         button_color=default_color_4, fg_color=default_color_2,
                                         dropdown_fg_color=default_color_1, dropdown_hover_color=default_color_2,
                                         dropdown_font=('Courier', 17), dropdown_text_color="black")
        self.game_list.pack(side="top")
        self.game_list.set("Sudoku")  # Default selection
        self.show_frame("Sudoku")  # Default show Sudoku

    def show_frame(self, name):
        """Bring the selected game frame to the top for display."""
        frame = self.frames[name]
        frame.tkraise()

    def change_game(self, event=None):
        """Function to change the game based on combobox selection."""
        game_name = self.game_list.get()
        self.show_frame(game_name)


if __name__ == "__main__":
    app = MainFrame()
    app.mainloop()
