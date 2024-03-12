from calculate import index_to_coord
from PIL import ImageTk, Image
import constants


class Ant:
    def __init__(self, i, j, canvas, name):
        self.canvas = canvas
        self.i = i
        self.j = j
        x, y = index_to_coord(i, j)
        self.x = constants.HEX_FIELD_X0 + x
        self.y = constants.HEX_FIELD_Y0 + y
        self.cell_size = constants.ANT_CELL_SIZE
        # self.image_selected_False = Image.open("image/ant.png").resize((self.cell_size, self.cell_size))
        # self.image_selected_True = Image.open("image/ant.png").resize((self.cell_size*2, self.cell_size*2))
        self.image_selected_False = Image.open("image/ant.png").resize((self.cell_size, self.cell_size))
        self.image_selected_True = Image.open("image/ant.png").resize((50, 50))
        self.img_selected_False = ImageTk.PhotoImage(self.image_selected_False)
        self.img_selected_True = ImageTk.PhotoImage(self.image_selected_True)
        self.obj = self.canvas.create_image(self.x, self.y, anchor='center', image=self.img_selected_False)
        self.selected = False
        self.color_selected = ''
        self.name = name

    def move_obj(self, event):
        new_x = event.x
        new_y = event.y
        if self.selected:
            self.choise_hex(new_x, new_y)
            self.canvas.coords(self.obj, self.x, self.y)
            print(self.name, 'перемещён')
            self.selected = False
            self.canvas.itemconfig(self.obj, image=self.img_selected_False)
            self.do_visible_ant()

    def choise_hex(self, x, y):
        for hex in self.canvas.hex_list:
            if ((x - hex.x) ** 2 + (y - hex.y) ** 2 <= constants.HEX_h ** 2
                    and (self.x - hex.x) ** 2 + (self.y - hex.y) ** 2 <= 6 * constants.HEX_h ** 2):
                # Позволяет передвигаться ТОЛЬКО на ближайшие хексы
                self.i = hex.i
                self.j = hex.j
                self.x = hex.x
                self.y = hex.y

    def do_visible_ant(self):
        for elem_hex in self.canvas.hex_list:
            if [elem_hex.i, elem_hex.j] == [self.i, self.j] and elem_hex.visible == False:
                self.canvas.itemconfig(elem_hex.obj, fill=constants.GREEN)
                elem_hex.visible = True
                print("видимость гекса", elem_hex.i, elem_hex.j)

    #     for ant in self.ant_list:
    #         if ant.selected is True:
    #             self.itemconfig(ant.obj, fill=constants.GREEN)
    #             ant.visible = True
