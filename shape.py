from PIL import ImageTk, Image
import constants


class Shape:
    instances = []

    def __init__(self, canvas, hexagon):
        self.canvas = canvas
        self.native_hex = hexagon
        self.i, self.j = hexagon.i, hexagon.j
        self.x, self.y = self.native_hex.x, self.native_hex.y
        self.obj = None

    def set_attributes(self, other, *attrs):
        for attr in attrs:
            if hasattr(other, attr):
                setattr(self, attr, getattr(other, attr))

    def has_matching_indexes_with(self, shape):
        return (self.i, self.j) == (shape.i, shape.j)

    def destroy_shape(self):
        self.canvas.delete(self.obj)  # Удаляет картинку
        self.instances.remove(self)  # Удаляет из списка элементов
        del self  # Удаляет экземпляр класса


class Ant(Shape):
    instances = []

    def __init__(self, canvas, hexagon, name):
        super().__init__(canvas, hexagon)
        self.cell_size = constants.ANT_CELL_SIZE
        self.color_selected = ''
        self.name = name
        self.carries = None  # содержит ОБЪЕКТ загруженной ягоды
        self.stuck = None  # содержит ОБЪЕКТ паутины или паука
        self.selected = False
        self._load_images()
        self.obj = self.canvas.create_image(self.x, self.y, anchor='center', image=self.get_image())
        self.instances.append(self)

    def _load_images(self):
        original_image = Image.open("image/ant.png")
        selected_image = ImageTk.PhotoImage(original_image.resize((50, 50)))
        deselected_image = ImageTk.PhotoImage(original_image.resize((self.cell_size, self.cell_size)))
        self._image = {'selected': selected_image, 'deselected': deselected_image}

    def get_image(self):
        return self._image['selected'] if self.selected else self._image['deselected']

    def select(self):
        self.selected = True
        self.canvas.itemconfig(self.obj, image=self.get_image())

    def deselect(self):
        self.selected = False
        self.canvas.itemconfig(self.obj, image=self.get_image())

    def move(self, hexagon):
        self.set_attributes(hexagon, 'i', 'j', 'x', 'y')
        self.canvas.coords(self.obj, self.x, self.y)
        print(self.name, 'перемещён', (self.i, self.j))
        self.show_hex()  # Открываем невидимый гекс
        if self.carries:  # Тащим ягоду
            self.carries.transfer(self.x, self.y - constants.OFFSET_TOP_Y_BERRY, self)

    def find_and_interact(self, objects, message_format, set_stuck=False):
        """Выводит сообщение и может стакать"""
        for obj in objects:
            if self.has_matching_indexes_with(obj):
                if not obj.visible:
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
        hexagon = self.canvas.hexes_dict.get((self.i, self.j))
        if not hexagon.visible:
            hexagon.make_visible()
            print("стал видимым гекс: ", (hexagon.i, hexagon.j))
        self.find_and_interact(Berry.instances, "{} нашёл {}", set_stuck=False)
        self.find_and_interact(Web.instances, "{} попал в паутину {}{}", set_stuck=True)
        self.find_and_interact(Spider.instances, "{} захвачен пауком {}{}", set_stuck=True)


class Berry(Shape):
    instances = []
    count = 0

    def __init__(self, canvas, hexagon):
        super().__init__(canvas, hexagon)
        self.obj = None
        self.visible = False
        self.taken = False
        self._load_images()
        self.name = constants.BERRIES_NAMES[Berry.count]
        Berry.count += 1
        self.instances.append(self)

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
        self.canvas.itemconfig(self.obj, image=self.get_image())

    def throw(self):
        self.taken = False
        self.canvas.itemconfig(self.obj, image=self.get_image())

    def transfer(self, ant_x, ant_y, ant):
        self.set_attributes(ant, 'i', 'j')
        self.canvas.coords(self.obj, ant_x, ant_y)
        print(f'{self.name.capitalize()} перемещена')


class Web(Shape):
    instances = []
    count = 0

    def __init__(self, canvas, hexagon):
        super().__init__(canvas, hexagon)
        Web.count += 1
        self.id = self.count
        self.visible = False
        self.obj = None
        self._load_images()
        self.instances.append(self)

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
    instances = []
    count = 0

    def __init__(self, canvas, hexagon):
        super().__init__(canvas, hexagon)
        Spider.count += 1
        self.id = self.count
        self.visible = False
        self.obj = None
        self._load_images()
        self.instances.append(self)

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
