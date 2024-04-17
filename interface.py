from tkinter import Button, Label
from tkinter import ttk
import constants


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
        super().__init__(canvas, text=time, font=("Helvetica", 15), foreground='blue', bg="lightgray")
        self.canvas = canvas
        self.time = time
        self.place(x=constants.WIDTH_WINDOW // 2, y=y, anchor='n')
        self.update_timer()

    def format_time(self, seconds):
        minutes, sec = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "{:01d}:{:02d}".format(minutes, sec)

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


class GameProgressbar(ttk.Progressbar):
    # втроенные цвета https://www.plus2net.com/python/tkinter-colors.php
    def __init__(self, canvas, time, x, y):
        super().__init__(
            canvas,
            orient="horizontal",
            length=constants.WIDTH_WINDOW * 0.7,  # ширина полосы
            mode="determinate"
        )
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("Horizontal.TProgressbar",
                             background=constants.GREEN,    # цвет полосы
                             troughcolor="lightgray",       # цвет фона
                             bordercolor="darkgray",        # цвет всех рамок
                             lightcolor="green",            # цвет вверха полосы
                             darkcolor="green")             # цвет низа полосы
        self.canvas = canvas
        self.time_to_start = time
        self.time = time
        self.place(x=constants.WIDTH_WINDOW // 2, y=y, anchor='n')
        self.start_progress()

    def start_progress(self):
        if self.time >= 0:
            self.time -= 1
            value = round(self.time * 100 / self.time_to_start, 1)
            self.config(value=value)
            self.after(1000, self.start_progress)
            if value < 10:
                self.style.configure("Horizontal.TProgressbar", background='brown2')
