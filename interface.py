from tkinter import Button



class UserButton(Button):
    def __init__(self, canvas, text):
        super().__init__(canvas, text=text, command=self.unvisible)

    def visible(self):
        self.place(x=100, y=800)

    def unvisible(self):
        self.destroy()