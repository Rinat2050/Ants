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
        self.loading = False

    def move_obj(self, event):
        new_x = event.x
        new_y = event.y
        if self.selected:
            self.choise_hex(new_x, new_y)
            self.canvas.coords(self.obj, self.x, self.y)
            print(self.name, 'перемещён')
            self.selected = False
            self.canvas.itemconfig(self.obj, image=self.photo_selected_False)
            self.do_visible_hex()
            try:
                self.canvas.btn_list[-1].destroy()
                self.canvas.btn_list.pop()
            except:
                print('Пустой список')

    def choise_hex(self, x, y):
        for hex_val in self.canvas.hex_dict.values():
            if ((x - hex_val.x) ** 2 + (y - hex_val.y) ** 2 <= constants.HEX_h ** 2
                    and (self.x - hex_val.x) ** 2 + (self.y - hex_val.y) ** 2 <= 6 * constants.HEX_h ** 2):
                # Позволяет передвигаться ТОЛЬКО на ближайшие хексы
                self.i = hex_val.i
                self.j = hex_val.j
                self.x = hex_val.x
                self.y = hex_val.y

    def do_visible_hex(self):
        for hex_val in self.canvas.hex_dict.values():
            if [hex_val.i, hex_val.j] == [self.i, self.j] and hex_val.visible is False:
                self.canvas.itemconfig(hex_val.obj, fill=constants.GREEN)
                hex_val.visible = True
                print("видимость гекса", hex_val.i, hex_val.j)

    #     for ant in self.ant_list:
    #         if ant.selected is True:
    #             self.itemconfig(ant.obj, fill=constants.GREEN)
    #             ant.visible = True


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
    def __init__(self, i, j, canvas):
        super().__init__(i, j, canvas)
        self.image_selected_False = Image.open("image/berry.png").resize((15, 15))
        self.image_selected_True = Image.open("image/berry.png").resize((25, 25))
        self.photo_selected_False = ImageTk.PhotoImage(self.image_selected_False)
        self.photo_selected_True = ImageTk.PhotoImage(self.image_selected_True)

        # self.image = Image.open("image/berry.png").resize((20, 20))
        # self.photo_image = ImageTk.PhotoImage(self.image)
        self.obj = self.canvas.create_image(self.x, self.y - 20, anchor='center', image=self.photo_selected_False)
        self.taken = False
