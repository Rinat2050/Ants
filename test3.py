# Нарисовать открытку с Новым годом.

from tkinter import *
from hexes import Hex

window = Tk()
window.title('модуль')
window.geometry('500x500+1200+300')

canvas = Canvas(window, width=1000, height=1000, bg='white')
canvas.grid(row=0, column=0)

canvas.create_line(1, 1, 500, 1)
for i in range(0, 501, 10):
    canvas.create_line(i, 1, i, 8)
    if i % 50 == 0:
        canvas.create_text(i, 10, text=i, justify=CENTER, font="Verdana 8")
    canvas.create_line(1, i, 8, i)
    if i % 50 == 0:
        canvas.create_text(20, i, text=i, justify=CENTER, font="Verdana 8")


def coord(event):
    window.title(f'x={event.x}, y={event.y}, {hex.click_is_inside(event.x, event.y)}')
    if hex.click_is_inside(event.x, event.y):
        canvas.create_oval(event.x-1, event.y-1, event.x+1, event.y+1, fill="black")


def coord2(event):
    x, y = event.x, event.y
    print(f'x={x}, y={y}')
    canvas.create_oval(x - 1, y - 1, x + 1, y + 1, outline='red')
    canvas.create_text(x, y, text=f'x={x}, y={y}', font="Verdana 8", anchor=SW)



hex = Hex((200, 200), canvas)
hex.center_to_six_vertex()

window.bind('<Motion>', coord)
window.bind('<Button-1>', coord2)

window.mainloop()

