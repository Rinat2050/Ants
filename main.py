# TODO: Если время вышло - бесполезно кликать.
# TODO: Сделать messagebox game over
# TODO: Улучшить coord_to_index
# TODO: Сделать игровой счёт: (длина списка ягод в доме / всего ягод)
# TODO: Кнопки привести в порядок

# После изготовления игры
# TODO: сделать вторую версию с уменьшенным полем и уменьшенным муравейником
# TODO: сделать версию с пчёлами Улей


from tkinter import Tk
import constants
from field import Field
from interface import Interface

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
user_panel = Interface(place_hex)

place_hex.bind('<Button-3>', place_hex.activate)
place_hex.bind('<Button-1>', place_hex.operate)

# Тестирование функции hex.is_hex()
# def coord(event):
#     hex = place_hex.hexes.hexes_dict[(0, 0)]
#     print(hex)
#     if hex.is_hex(event.x, event.y):
#         place_hex.create_oval(event.x-1, event.y-1, event.x+1, event.y+1, fill="black")
#     window.title(f'x={event.x}, y={event.y}, {hex.is_hex(event.x, event.y)}')
#
# place_hex.bind('<Motion>', coord)

window.mainloop()
