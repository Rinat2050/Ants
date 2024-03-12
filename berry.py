from calculate import index_to_coord
from PIL import ImageTk, Image
import constants

class Berry:
    def __init__(self, i, j, canvas):
        self.canvas = canvas
        self.i = i
        self.j = j
        x, y = index_to_coord(i, j)
        self.x = constants.HEX_FIELD_X0 + x
        self.y = constants.HEX_FIELD_Y0 + y
        self.image = Image.open("image/berry.png").resize((20, 20))
        self.photo_image = ImageTk.PhotoImage(self.image)
        self.obj = self.canvas.create_image(self.x, self.y, anchor='center', image=self.photo_image)
        self.taken = False


