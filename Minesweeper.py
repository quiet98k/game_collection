import random
import tkinter as tk
import customtkinter as ctk

default_color_1 = "#e8e8e8"
default_color_2 = "#b7b7b7"
default_color_3 = "#8c8c8c"
default_color_4 = "#525252"


class Minesweeper(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.num = 16  # Number of cells in a row and column
        self.num_of_mines = 0

        self.configure(fg_color=default_color_3, width=900, height=900)
        self.pack_propagate(False)  # Prevent the frame from resizing to fit its content

        # Create a frame to hold the grid of buttons
        main_grid_frame = ctk.CTkFrame(self, fg_color='black', border_width=1)
        main_grid_frame.pack(fill="both", expand=True)
        main_grid_frame.grid_propagate(False)  # Prevent the frame from resizing to fit its content

        # Use update_idletasks to ensure the frame dimensions are updated
        self.parent.update_idletasks()
        frame_width = main_grid_frame.winfo_width()  # Get the frame's width
        frame_height = main_grid_frame.winfo_height()  # Get the frame's height

        square_width = frame_width // self.num  # Calculate the width of each square
        square_height = frame_height // self.num  # Calculate the height of each square

        # Create a 2D list of buttons for the grid
        self.gameGrid = [[None for _ in range(self.num)] for _ in range(self.num)]

        for i in range(self.num):
            for j in range(self.num):
                self.gameGrid[i][j] = ctk.CTkButton(main_grid_frame, text=str(random.randint(1, 9)),
                                                    font=('Courier', 40),
                                                    fg_color=default_color_1, border_width=1, border_color="black",
                                                    hover_color=default_color_2, corner_radius=0, text_color="black")
                self.gameGrid[i][j].grid(row=i, column=j, sticky="nsew")
                self.gameGrid[i][j].bind("<Button-1>", self.left_click)
                self.gameGrid[i][j].bind("<Button-3>", self.right_click)
                main_grid_frame.grid_columnconfigure(j, weight=1)
                main_grid_frame.grid_rowconfigure(i, weight=1)

    def left_click(self, event):
        print(event.widget)

    def right_click(self, event):
        event.widget.configure(fg_color="red")
