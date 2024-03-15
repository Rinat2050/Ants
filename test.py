import tkinter as tk

def command1(event):
    print("Command 1")

def command2(event):
    print("Command 2")

def command3(event):
    print("Command 3")

root = tk.Tk()
canvas = tk.Canvas(root, width=200, height=200)
canvas.pack()

button = tk.Button(root, text="Click me!")
button.pack()

button.bind("<Button-1>", lambda event: [command1(event), command2(event), command3(event)])

root.mainloop()
