# TODO: find_neighbors должна показывать только существующие
# TODO: упростить добавление новых муравьёв. Сейчас надо не только создать объект, но и добавить его в список вручную
# TODO: дописать Place/def ant_direction
# TODO: заменить таймер "полосой загрузки" Progressbar
# TODO: разместить паутинки СЛУЧАЙНО на предпоследнем круге
# TODO: разместить пауков СЛУЧАЙНО на последнем круге
# TODO: вместо клика правой - наведение курсора
# TODO: переименовать функции и переменные
# TODO: Пауки и паутины НЕ должны быть на 1 клетке. Заменить hex.enemy на hex.loading?
# TODO: списки объектов должны автоматом создаваться при создании. Хранятся в классе
# TODO: field/ant._find_a... строка 46. Муравей теперь стакается, но... с помощью запрещённой функции
# TODO: При клике на застаканного муравья правой, паутина становися ярче!
# TODO: При клике на застаканного муравья правой, продолжает писаться лог

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

window.mainloop()
