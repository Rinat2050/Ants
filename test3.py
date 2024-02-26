from tkinter import *

class Ant:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.ant = self.canvas.create_oval(x, y, x + 10, y + 10, fill='black')
        self.canvas.bind("<Button-1>", self.move_ant)

    def move_ant(self, event):
        new_x = event.x - 5
        new_y = event.y - 5
        self.canvas.coords(self.ant, new_x, new_y, new_x + 10, new_y + 10)

root = Tk()
canvas = Canvas(root, width=300, height=300, bg='white')
canvas.pack()

ant = Ant(canvas, 100, 100)

root.mainloop()
