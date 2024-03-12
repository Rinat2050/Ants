from tkinter import Tk
import constants
from place import Place

window = Tk()
window.title('ANTS')
window.geometry('{w}x{h}+1100+0'.format(
    w=constants.WIDTH_WINDOW,
    h=constants.HEIGHT_WINDOW),
)


place_hex = Place(window)

window.mainloop()
