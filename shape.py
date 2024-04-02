from calculate import index_to_coord, compare_distance
from PIL import ImageTk, Image
from math import cos, sin, pi
import constants


class Shape:
    def __init__(self, index, canvas):
        self.canvas = canvas
        self.i, self.j = index
        x, y = index_to_coord(index)
        self.x = constants.HEX_FIELD_X0 + x
        self.y = constants.HEX_FIELD_Y0 + y

    def set_attributes(self, other, *attrs):
        for attr in attrs:
            if hasattr(other, attr):
                setattr(self, attr, getattr(other, attr))

    def has_matching_indexes_with(self, shape):
        return (self.i, self.j) == (shape.i, shape.j)


class Ant(Shape):
    def __init__(self, index, canvas, name):
        super().__init__(index, canvas)
        self.cell_size = constants.ANT_CELL_SIZE
        self.color_selected = ''
        self.name = name
        self.carries = None     # содержит ОБЪЕКТ загруженной ягоды
        self.stuck = None       # содержит ОБЪЕКТ паутины прилипалы
        self.selected = False
        self._load_images()
        self.obj = self.canvas.create_image(self.x, self.y, anchor='center', image=self.get_image())

    def _load_images(self):
        original_image = Image.open("image/ant.png")
        selected_image = ImageTk.PhotoImage(original_image.resize((50, 50)))
        deselected_image = ImageTk.PhotoImage(original_image.resize((self.cell_size, self.cell_size)))
        self._image = {'selected': selected_image, 'deselected': deselected_image}

    def get_image(self):
        return self._image['selected'] if self.selected else self._image['deselected']

    def select(self):
        self.selected = True

    def deselect(self):
        self.selected = False

    def move_obj(self, event):
        if not self.selected:
            print('Выберите муравья!')
            return
        self.selected = False
        self.choose_hex(event.x, event.y)
        self.canvas.coords(self.obj, self.x, self.y)
        print(self.name, 'перемещён')
        self.canvas.itemconfig(self.obj, image=self.get_image())
        self.show_hex()  # Открываем невидимый гекс
        if self.carries:  # Тащим ягоду
            self.carries.move_berry(self.x, self.y - constants.OFFSET_TOP_Y_BERRY, self)
        if len(self.canvas.btn_list) > 0:
            self.canvas.btn_list.pop().destroy()
            # TODO fix this, button must be destroyed from method where button was clicked

    def choose_hex(self, x, y):
        for hex in self.canvas.hexes_dict.values():
            if compare_distance((hex.x, hex.y), (x, y), '<=', constants.HEX_h) \
               and compare_distance((hex.x, hex.y), (self.x, self.y), '<=', 3*constants.HEX_h):
                self.set_attributes(hex, 'i', 'j', 'x', 'y')

    def _find_and_interact(self, objects, message_format, set_stuck=False):
        for obj in objects:
            if self.has_matching_indexes_with(obj) and not obj.visible:
                obj.show()
                print(message_format.format(
                    self.name,
                    obj.name if hasattr(obj, 'name') else '',
                    obj.id if hasattr(obj, 'id') else '')
                )
                if set_stuck:
                    self.stuck = True
                break

    def show_hex(self):
        hex = self.canvas.hexes_dict.get((self.i, self.j))
        if not hex or hex.visible:
            return
        hex.visible = True
        self.canvas.itemconfig(hex.obj, fill=constants.GREEN)
        print("стал видимым гекс: ", hex.i, hex.j)

        self._find_and_interact(self.canvas.berries, "{} нашёл {}", set_stuck=False)
        self._find_and_interact(self.canvas.cobwebs, "{} нашёл паутину :( {}", set_stuck=True)
        self._find_and_interact(self.canvas.spiders, "{} нашёл паука :( {}", set_stuck=True)


class Hex(Shape):
    def __init__(self, index, canvas):
        super().__init__(index, canvas)
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
    count = 0
    def __init__(self, index, canvas):
        super().__init__(index, canvas)
        self.obj = None
        self.visible = False
        self.taken = False
        self._load_images()
        self.name = constants.BERRIES_NAMES[Berry.count]
        Berry.count += 1

    def _load_images(self):
        original_image = Image.open("image/berry.png")
        taken_image = ImageTk.PhotoImage(original_image.resize((7, 7)))
        free_image = ImageTk.PhotoImage(original_image.resize((15, 15)))
        self._image = {'taken': taken_image, 'free': free_image}

    def get_image(self):
        return self._image['taken'] if self.taken else self._image['free']

    def show(self):
        self.visible = True
        self.obj = self.canvas.create_image(self.x, self.y - constants.OFFSET_TOP_Y_BERRY,
                                            anchor='center', image=self.get_image())

    def take(self):
        self.taken = True

    def throw(self):
        self.taken = False

    def move_berry(self, ant_x, ant_y, ant):
        self.set_attributes(ant, 'i', 'j')
        self.canvas.coords(self.obj, ant_x, ant_y)
        print(self.name, 'перемещена')


class Web(Shape):
    count = 0

    def __init__(self, index, canvas):
        super().__init__(index, canvas)
        self.count += 1
        self.id = self.count
        self.visible = False
        self.obj = None
        self._load_images()

    def _load_images(self):
        original_image = Image.open("image/web.png")
        image = ImageTk.PhotoImage(original_image.resize((30, 30)))
        self._image = image

    def get_image(self):
        return self._image

    def show(self):
        self.visible = True
        self.obj = self.canvas.create_image(self.x, self.y,
                                            anchor='center', image=self.get_image())


class Spider(Shape):
    count = 0

    def __init__(self, index, canvas):
        super().__init__(index, canvas)
        self.count += 1
        self.id = self.count
        self.visible = False
        self.obj = None
        self._load_images()

    def _load_images(self):
        original_image = Image.open("image/spider.png")
        image = ImageTk.PhotoImage(original_image.resize((30, 30)))
        self._image = image

    def get_image(self):
        return self._image

    def show(self):
        self.visible = True
        self.obj = self.canvas.create_image(self.x, self.y,
                                            anchor='center', image=self.get_image())
