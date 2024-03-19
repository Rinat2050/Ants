from tkinter import Button


class UserButton(Button):
    def __init__(self, canvas, text, x, y):
        super().__init__(text=text, command=self.click_to_act)
        self.canvas = canvas
        self.visible(x, y)

    def visible(self, x, y):
        self.place(x=x, y=y)

    def click_to_act(self):
        self.destroy()


class TakeButton(UserButton):
    def __init__(self, canvas, text, x, y):
        super().__init__(canvas, text, x, y)

    def click_to_act(self):
        self.canvas.ant_takes_berry()
        self.destroy()


class DropButton(UserButton):
    def __init__(self, canvas, text, x, y):
        super().__init__(canvas, text, x, y)

    def click_to_act(self):
        self.canvas.ant_drops_berry()
        self.destroy()
