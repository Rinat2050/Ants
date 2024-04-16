# Import necessary modules
import tkinter
from tkinter import ttk
from tkinter import Tk
from tkinter import ttk
# Create the main application window
root = Tk()
root.title("Adventurer's Progress")
# Access the ttk.Style() object
style = ttk.Style()
# Set the theme to "clam"
style.theme_use("clam")
# Configure the Horizontal.TProgressbar style in "clam" theme
style.configure("Horizontal.TProgressbar",
 background="lightblue",
 troughcolor="lightgray",
 bordercolor="darkblue",
 lightcolor="lightblue",
 darkcolor="darkblue")
# Configure the Vertical.TProgressbar style in "clam" theme
style.configure("Vertical.TProgressbar",
 background="lightyellow",
 troughcolor="lightgray",
 bordercolor="darkorange",
 lightcolor="lightyellow",
 darkcolor="darkorange")
horizontal_progressbar = ttk.Progressbar(root, length=200, value=50, orient="horizontal")
horizontal_progressbar.pack()
vertical_progressbar = ttk.Progressbar(root, length=200, value=50, orient="vertical")
vertical_progressbar.pack()
# Start the main event loop
root.mainloop()