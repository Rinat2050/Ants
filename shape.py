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
        self.loading = None

    def move_obj(self, event):
        new_x = event.x
        new_y = event.y

        if self.selected:
            self.choise_hex(new_x, new_y)
            self.canvas.coords(self.obj, self.x, self.y)
            print(self.name, 'перемещён')
            self.selected = False
            self.canvas.itemconfig(self.obj, image=self.photo_selected_False)

            self.do_visible_hex()       # Открываем невидимый гекс

            if self.loading:            # Тащим ягоду
                self.loading.move_berry(self.x, self.y - constants.OFFSET_TOP_Y_BERRY, self)

            try:
                self.canvas.btn_list[-1].destroy()
                self.canvas.btn_list.pop()
            except:
                pass

    def choise_hex(self, x, y):
        for hex_val in self.canvas.hexes_dict.values():
            if ((x - hex_val.x) ** 2 + (y - hex_val.y) ** 2 <= constants.HEX_h ** 2
                    and (self.x - hex_val.x) ** 2 + (self.y - hex_val.y) ** 2 <= 6 * constants.HEX_h ** 2):
                # Позволяет передвигаться ТОЛЬКО на ближайшие хексы
                self.i = hex_val.i
                self.j = hex_val.j
                self.x = hex_val.x
                self.y = hex_val.y

    def do_visible_hex(self):
        for hex_val in self.canvas.hexes_dict.values():
            if [hex_val.i, hex_val.j] == [self.i, self.j] and hex_val.visible is False:
                self.canvas.itemconfig(hex_val.obj, fill=constants.GREEN)
                hex_val.visible = True
                print("стал видимым гекс: ", hex_val.i, hex_val.j)
                berry = self.canvas.berries_dict.get((self.i, self.j), None)
                if berry and not berry.visible:
                    berry.do_visible_berry()
                    print(self.name, 'нашёл', berry.name)


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
        self.image_selected_True = Image.open("image/berry.png").resize((25, 25))
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
        self.canvas.berries_dict[(ant.i, ant.j)] = self.canvas.berries_dict.pop((self.i, self.j))
        self.i = ant.i
        self.j = ant.j
        self.canvas.coords(self.obj, ant_x, ant_y)
        print(self.name, 'перемещена')
