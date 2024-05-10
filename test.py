import random
import tkinter as tk
import customtkinter as ctk
from PIL import Image

default_color_1 = "#e8e8e8"
default_color_2 = "#b7b7b7"
default_color_3 = "#8c8c8c"
default_color_4 = "#525252"

app = ctk.CTk()
app.geometry("600x500")
app.title("CTk example")
my_image = ctk.CTkImage(light_image=Image.open("mine.png"))

image_label = ctk.CTkButton(app, image=my_image, text="")  # display image with a CTkLabe
image_label.pack()

app.mainloop()