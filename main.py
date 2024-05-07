# TODO: Warnings сообщения сделать Синглтон

# После изготовления игры
# TODO: сделать вторую версию с уменьшенным полем и уменьшенным муравейником
# TODO: сделать версию с пчёлами Улей


from tkinter import Tk
import constants
from field import Field
from interface import Interface
from shape import Berry, Web, Spider

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
place_hex.do_visible_hexes(place_hex.hexes_dict[0, 0], constants.VISIBLE_ROUND)
place_hex.create_anthill()
place_hex.create_group_of_ants(constants.NUMBER_OF_ANTS)
place_hex.create_random_objects(Web, constants.NUMBER_OF_COBWEBS, 'is_anthill', 'load')
place_hex.create_random_objects(Spider, constants.NUMBER_OF_SPIDERS, 'is_anthill', 'load')
place_hex.create_random_objects(Berry, constants.NUMBER_OF_BERRIES, 'is_anthill', 'load')
user_panel = Interface(place_hex)
user_panel.progressbar.start_progress()

place_hex.bind('<Button-3>', place_hex.activate)
place_hex.bind('<Button-1>', place_hex.operate)

window.mainloop()
