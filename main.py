# TODO: иногда приходиться кликать правой дважды
# TODO: берёт ягоды в муравейнике. Запретить?

from tkinter import Tk
import constants
from place import Place


window = Tk()
window.title('ANTS')

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_offset = (screen_width - constants.WIDTH_WINDOW)
y_offset = (screen_height - constants.HEIGHT_WINDOW) * 0

window.geometry('{w}x{h}+{x}+{y}'.format(
    w=constants.WIDTH_WINDOW,
    h=constants.HEIGHT_WINDOW,
    x=x_offset,
    y=y_offset,
))

place_hex = Place(window)

window.mainloop()
