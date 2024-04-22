# TODO: меняются ли ij ягод при перетаскивании?
# TODO: при перемещении муравья заменять привязку к гексу
# TODO: упростить добавление новых муравьёв. Сейчас надо не только создать объект, но и добавить его в список вручную
# TODO: дописать Place/def ant_direction
# TODO: вместо клика правой - наведение курсора. Выбирать гексы, но выделять муравьёв
# TODO: field/ant._find_a... строка 46. Муравей теперь стакается, но... с помощью запрещённой функции
# TODO: Если время вышло - бесполезно кликать
# TODO: Улучшить coord_to_index

# После изготовления игры
# TODO: сделать вторую версию с уменьшенным полем и уменьшенным муравейником
# TODO: сделать версию с пчёлами Улей


from tkinter import Tk
import constants
from field import Field

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

place_hex = Field(window)
place_hex.bind('<Button-3>', place_hex.activate)
place_hex.bind('<Button-1>', place_hex.operate)
window.mainloop()
