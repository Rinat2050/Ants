# TODO: упростить добавление новых муравьёв. Сейчас надо не только создать объект, но и добавить его в список вручную
# TODO: дописать Place/def ant_direction
# TODO: заменить таймер "полосой загрузки"
# TODO: разместить паутинки СЛУЧАЙНО на предпоследнем круге
# TODO: разместить пауков СЛУЧАЙНО на последнем круге
# TODO: вместо клика правой - наведение курсора
# TODO: переименовать функции и переменные


# TODO: сделать вторую версию с уменьшенным полем и уменьшенным муравейником

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
