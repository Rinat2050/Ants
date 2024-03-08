import tkinter as tk

class Shape:
    def __init__(self, canvas, shape_type, x1, y1, x2, y2):
        self.canvas = canvas
        self.shape_type = shape_type
        self.shape = None
        self.selected = False
        if shape_type == 'circle':
            self.shape = canvas.create_oval(x1, y1, x2, y2, outline='black', width=2)
        elif shape_type == 'square':
            self.shape = canvas.create_rectangle(x1, y1, x2, y2, outline='black', width=2)
        self.canvas.tag_bind(self.shape, '<Button-1>', self.select_shape)
        self.canvas.tag_bind(self.shape, '<B1-Motion>', self.move_shape)

    def select_shape(self, event):
        self.canvas.itemconfig(self.shape, outline='red')
        for shape in shapes:
            if shape != self:
                shape.canvas.itemconfig(shape.shape, outline='')
                shape.selected = False
        self.selected = True

    def move_shape(self, event):
        if self.selected:
            x, y = event.x, event.y
            self.canvas.coords(self.shape, x - 25, y - 25, x + 25, y + 25)

root = tk.Tk()
root.title('Select and Move Shapes')

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

shapes = [
    Shape(canvas, 'circle', 150, 150, 250, 250),
    Shape(canvas, 'square', 50, 50, 100, 100)
]

root.mainloop()
