from tkinter import Button, Label
from tkinter import ttk
from tkinter.messagebox import showinfo
import constants


class Interface:
    def __init__(self, canvas):
        self.canvas = canvas
        self.timer = Timer(self.canvas, constants.TIME, constants.WIDTH_WINDOW // 2, 70)
        self.progressbar = GameProgressbar(self.canvas, constants.TIME, constants.WIDTH_WINDOW // 2, 40)
        self.score = Score(self.canvas, constants.WIDTH_WINDOW // 2, 110)


class UserButton(Button):
    btn_list = []

    def __init__(self, canvas, text, current_hex):
        super().__init__(text=text, bg='green', activebackground='green', command=self.on_click)
        self.canvas = canvas
        self.hex = current_hex
        self.place(x=self.hex.x, y=self.hex.y, anchor='n')
        UserButton.btn_list.append(self)

    def on_click(self):
        self.destroy()

    def destroy_list(self):
        for btn in self.btn_list:
            btn.destroy()
        self.btn_list.clear()


class HelpButton(UserButton):
    def __init__(self, canvas, text, current_hex, selected_ant):
        super().__init__(canvas, text, current_hex)
        self.selected_ant = selected_ant

    def on_click(self):
        self.selected_ant.deselect()
        self.canvas.ant_help_friend(self.hex)
        self.hex.load.destroy_shape()
        UserButton.destroy_list(self)


class TakeButton(UserButton):
    def __init__(self, canvas, text, current_hex):
        super().__init__(canvas, text, current_hex)

    def on_click(self):
        self.canvas.ant_takes_berry(self.hex)
        self.destroy()


class DropButton(UserButton):
    def __init__(self, canvas, text, current_hex):
        super().__init__(canvas, text, current_hex)

    def on_click(self):
        self.canvas.ant_drops_berry(self.hex)
        UserButton.destroy_list(self)
        Score.instance.update()


class Timer(Label):
    def __init__(self, canvas, time, x, y):
        super().__init__(canvas, text=time, font=("Helvetica", 15), foreground='blue', bg="lightgray")
        self.canvas = canvas
        self.time_to_start = time
        self.time = time
        self.x, self.y = x, y
        self.place(x=self.x, y=self.y, anchor='n')
        self.msg = None
        self.update()

    @staticmethod
    def format_time(seconds):
        minutes, sec = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return "{:01d}:{:02d}".format(minutes, sec)

    def update(self):
        if self.time > 0:
            time_str = self.format_time(self.time)
            self.config(text=time_str)
            self.time -= 1
            self.after(1000, self.update)
            if self.time * 100 / self.time_to_start < 20:
                self.config(foreground='red')
        elif Score.finish is False:
            Score.finish = True
            self.config(text="Время вышло!")
            self.msg = Message('Игра окончена.')
            self.msg.open_warning()


class Score(Label):
    instance = None
    finish = False

    def __init__(self, canvas, x, y):
        super().__init__(canvas, font=("Helvetica", 15), foreground='blue', bg="lightgray")
        self.canvas = canvas
        self.x, self.y = x, y
        self.place(x=self.x, y=self.y, anchor='n')
        self.count = len(self.canvas.hexes.hexes_dict[(0, 0)].warehouse)
        self.config(text=f'{self.count} / {constants.NUMBER_OF_BERRIES}')
        self.msg = None
        Score.instance = self

    def update(self):
        self.count = len(self.canvas.hexes.hexes_dict[(0, 0)].warehouse)
        self.config(text=f'{self.count} / {constants.NUMBER_OF_BERRIES}')
        if self.count == constants.NUMBER_OF_BERRIES and Score.finish is False:
            Score.finish = True
            self.msg = Message('Поздравляем! Вы победили!')
            self.msg.open_warning()


class GameProgressbar(ttk.Progressbar):
    # встроенные цвета https://www.plus2net.com/python/tkinter-colors.php
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
                             background=constants.GREEN,  # цвет полосы
                             troughcolor="lightgray",  # цвет фона
                             bordercolor="darkgray",  # цвет всех рамок
                             lightcolor="green",  # цвет верха полосы
                             darkcolor="green")  # цвет низа полосы
        self.canvas = canvas
        self.time_to_start = time
        self.time = time
        self.x, self.y = x, y
        self.place(x=self.x, y=self.y, anchor='n')

    def start_progress(self):
        if self.time >= 0:
            self.time -= 1
            value = round(self.time * 100 / self.time_to_start, 1)
            self.config(value=value)
            self.after(1000, self.start_progress)
            if value < 20:
                self.style.configure("Horizontal.TProgressbar", background='brown2')


class Message:
    def __init__(self, text):
        self.text = text

    def open_warning(self):
        showinfo(title="Конец",
                 message=f'{self.text}\n'
                         f'Собрано ягод: {Score.instance.count} из {constants.NUMBER_OF_BERRIES}\n'
                 )
