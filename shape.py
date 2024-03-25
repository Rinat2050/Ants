from calculate import index_to_coord
from PIL import ImageTk, Image
from math import cos, sin, pi
import constants


class Shape:
    def __init__(self, i, j, canvas):
        self.canvas = canvas
        self.i = i
        self.j = j
        x, y = index_to_coord(i, j)
        self.x = constants.HEX_FIELD_X0 + x
        self.y = constants.HEX_FIELD_Y0 + y

class Ant(Shape):
    def __init__(self, i, j, canvas, name):
        super().__init__(i, j, canvas)
        self.cell_size = constants.ANT_CELL_SIZE
        self.image_selected_False = Image.open("image/ant.png").resize((self.cell_size, self.cell_size))
        self.image_selected_True = Image.open("image/ant.png").resize((50, 50))
        self.photo_selected_False = ImageTk.PhotoImage(self.image_selected_False)
        self.photo_selected_True = ImageTk.PhotoImage(self.image_selected_True)
        self.obj = self.canvas.create_image(self.x, self.y, anchor='center', image=self.photo_selected_False)
        self.selected = False
        self.color_selected = ''
        self.name = name
        self.loading = None     # содержит ОБЪЕКТ загруженной ягоды
        self.stuck = None       # содержит ОБЪЕКТ паутины прилипалы


class Hex(Shape):
    def __init__(self, i, j, canvas):
        super().__init__(i, j, canvas)
        self.visible = True
        self.obj = self.canvas.create_polygon(
            self.count_coord(self.x, self.y),
            fill=constants.GREEN,
            outline="#004D40")
        self.canvas.create_text(self.x, self.y+20,
                                text=(self.i, ':', self.j),
                                fill="blue")
        self.is_anthill = False
        self.enemy = None

    @staticmethod
    def count_coord(center_x, center_y):
        coordinates = []
        for i in range(6):
            vertex_x = int(
                    center_x +
                    constants.HEX_LENGTH * cos(i * 2 * pi / 6)
                )
            vertex_y = int(
                    center_y +
                    constants.HEX_LENGTH * sin(i * 2 * pi / 6)
                )
            coordinates.append(vertex_x)
            coordinates.append(vertex_y)
        return coordinates


class Berry(Shape):
    def __init__(self, i, j, canvas, name):
        super().__init__(i, j, canvas)
        self.name = name
        self.image_selected_False = Image.open("image/berry.png").resize((15, 15))
        self.image_selected_True = Image.open("image/berry.png").resize((7, 7))
        self.photo_selected_False = ImageTk.PhotoImage(self.image_selected_False)
        self.photo_selected_True = ImageTk.PhotoImage(self.image_selected_True)
        self.visible = False
        self.obj = None
        self.taken = False

    def do_visible_berry(self):
        self.visible = True
        self.obj = self.canvas.create_image(self.x, self.y - constants.OFFSET_TOP_Y_BERRY,
                                            anchor='center', image=self.photo_selected_False)

    def move_berry(self, ant_x, ant_y, ant):
        self.i = ant.i
        self.j = ant.j
        self.canvas.coords(self.obj, ant_x, ant_y)
        print(self.name, 'перемещена')

class Web(Shape):
    count = 0
    def __init__(self, i, j, canvas):
        super().__init__(i, j, canvas)
        self.count += 1
        self.id = self.count
        self.image_selected_False = Image.open("image/web.png").resize((30, 30))
        #self.image_selected_True = Image.open("image/web.png").resize((7, 7))
        self.photo_selected_False = ImageTk.PhotoImage(self.image_selected_False)
        #self.photo_selected_True = ImageTk.PhotoImage(self.image_selected_True)
        self.visible = False
        self.obj = None

    def do_visible_web(self):
        self.visible = True
        self.obj = self.canvas.create_image(self.x, self.y,
                                            anchor='center', image=self.photo_selected_False)

class Spider(Shape):
    count = 0
    def __init__(self, i, j, canvas):
        super().__init__(i, j, canvas)
        self.count += 1
        self.id = self.count
        self.image_selected_False = Image.open("image/spider.png").resize((30, 30))
        #self.image_selected_True = Image.open("image/web.png").resize((7, 7))
        self.photo_selected_False = ImageTk.PhotoImage(self.image_selected_False)
        #self.photo_selected_True = ImageTk.PhotoImage(self.image_selected_True)
        self.visible = False
        self.obj = None

    def do_visible_spider(self):
        self.visible = True
        self.obj = self.canvas.create_image(self.x, self.y,
                                            anchor='center', image=self.photo_selected_False)

