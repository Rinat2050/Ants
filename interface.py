from tkinter import Button, Label
from tkinter import ttk
from tkinter.messagebox import showinfo
import constants


class Interface:
    def __init__(self, canvas):
        self.canvas = canvas
        self.create_score()
        self.create_timer(constants.TIME)
        self.create_progressbar(constants.TIME)

    def create_timer(self, time):
        self.timer = Timer(self.canvas, time, 999, 70)

    def create_progressbar(self, time):
        self.progressbar = GameProgressbar(self.canvas, time, 999, 40)

    def create_score(self):
        self.score = Score(self.canvas, 999, 110)


class UserButton(Button):
    btn_list = []

    def __init__(self, canvas, text, hex):
        super().__init__(text=text, bg='green', activebackground='green', command=self.on_click)
        self.canvas = canvas
        self.hex = hex
        self.place(x=hex.x, y=hex.y, anchor='n')
        UserButton.btn_list.append(self)

    def on_click(self):
        self.destroy()

    def destroy_list(self):
        for btn in self.btn_list:
            btn.destroy()
        self.btn_list.clear()


class HelpButton(UserButton):
    def __init__(self, canvas, text, hex, selected_ant):
        super().__init__(canvas, text, hex)
        self.selected_ant = selected_ant

    def on_click(self):
        self.selected_ant.deselect()
        self.canvas.ant_help_fried(self.hex)
        self.hex.load.destroy_shape()
        UserButton.destroy_list(self)


class TakeButton(UserButton):
    def __init__(self, canvas, text, hex):
        super().__init__(canvas, text, hex)

    def on_click(self):
        self.canvas.ant_takes_berry(self.hex)
        self.destroy()


class DropButton(UserButton):
    def __init__(self, canvas, text, hex):
        super().__init__(canvas, text, hex)

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
        self.place(x=constants.WIDTH_WINDOW // 2, y=y, anchor='n')
        self.update()


    def format_time(self, seconds):
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
        else:
            self.config(text="Время вышло!")
            self.warning = Message('Игра окончена.')


class Score(Label):
    instance = None
    win = False

    def __init__(self, canvas, x, y):
        super().__init__(canvas, font=("Helvetica", 15), foreground='blue', bg="lightgray")
        self.canvas = canvas
        self.place(x=constants.WIDTH_WINDOW // 2, y=y, anchor='n')
        self.count = 0
        self.update()
        Score.instance = self

    def update(self):
        self.count = len(self.canvas.hexes.hexes_dict[(0, 0)].warehouse)
        self.config(text=f'{self.count} / {constants.NUMBER_OF_BERRIES}')
        if self.count == constants.NUMBER_OF_BERRIES:
            self.warning = Message('Поздравляем! Вы победили!')
            Score.win = True


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
                             background=constants.GREEN,  # цвет полосы
                             troughcolor="lightgray",  # цвет фона
                             bordercolor="darkgray",  # цвет всех рамок
                             lightcolor="green",  # цвет вверха полосы
                             darkcolor="green")  # цвет низа полосы
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
            if value < 20:
                self.style.configure("Horizontal.TProgressbar", background='brown2')


class Message:
    def __init__(self, text):
        self.text = text
        self.open_warning()

    def open_warning(self):
        showinfo(title="Конец",
                message=f'{self.text}\n'
                        f'Собрано ягод: {Score.instance.count} из {constants.NUMBER_OF_BERRIES}\n'
                    )
