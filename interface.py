from tkinter import Button



class Interface:
    def __init__(self, canvas):
        self.btn_ant_take = Button(canvas, text="Взять", command=canvas.ant_take)
        self.btn_ant_take.place(x=100, y=800)

