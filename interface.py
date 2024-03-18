from tkinter import Button


class UserButton(Button):
    def __init__(self, canvas, text):
        super().__init__(text=text, command=self.unvisible)
        self.canvas = canvas

    def visible(self):
        self.place(x=100, y=800)

    def unvisible(self):
        self.canvas.ant_take()
        self.destroy()