from tkinter import Button, Label
from tkinter import ttk


class UserButton(Button):
    def __init__(self, canvas, text, x, y):
        super().__init__(text=text, bg='green', activebackground='green', command=self.on_click)
        self.canvas = canvas
        self.place(x=x, y=y, anchor='n')

    def on_click(self):
        self.destroy()


class TakeButton(UserButton):
    def __init__(self, canvas, text, x, y):
        super().__init__(canvas, text, x, y)

    def on_click(self):
        self.canvas.ant_takes_berry()
        self.destroy()


class DropButton(UserButton):
    def __init__(self, canvas, text, x, y):
        super().__init__(canvas, text, x, y)

    def on_click(self):
        self.canvas.ant_drops_berry()
        self.destroy()


class Timer(Label):
    def __init__(self, canvas, time, x, y):
        super().__init__(canvas, text=time, font=("Helvetica", 40), foreground='blue')
        self.canvas = canvas
        self.time = time
        self.place(x=x, y=y, anchor='n')
        self.update_timer()

    def format_time(self, seconds):
        minutes, sec = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "{:2d}:{:02d}".format(minutes, sec)

    def update_timer(self):
        if self.time > 0:
            time_str = self.format_time(self.time)
            self.config(text=time_str)
            self.time -= 1
            self.after(1000, self.update_timer)
            if self.time < 30:
                self.config(foreground='red')
        else:
            self.config(text="Время вышло!")


class Game_progressbar(ttk.Progressbar):
    def __init__(self, canvas, time, x, y):
        super().__init__(
            canvas,
            orient="horizontal",
            length=500,
            mode="determinate"
        )
        self.canvas = canvas
        self.time = time
        self.place(x=x, y=y, anchor='n')
        self.start(time)
        # self.step(500)
        self.after(time*500, self.stop)
        # value_var
        print(time)
