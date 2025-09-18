from tkinter import *
from time import strftime

TEXT_COLOR = "#00ffea"
GLOW_COLOR = "#003f3f"
BG_COLOR = "#000000"
FONT_STYLE = ("DS-Digital", 90, "bold")

root = Tk()
root.title("Digital Clock")
root.config(bg=BG_COLOR)

def time():
    string = strftime('%I:%M:%S %p')
    glow.config(text=string)
    label.config(text=string)
    label.after(1000, time)

glow = Label(root, font=FONT_STYLE, background=BG_COLOR, foreground=GLOW_COLOR)
glow.pack(anchor='center', pady=20, padx=20)

label = Label(root, font=FONT_STYLE, background=BG_COLOR, foreground=TEXT_COLOR)
label.place(relx=0.5, rely=0.5, anchor="center")

time()

mainloop()
