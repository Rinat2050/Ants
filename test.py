import tkinter as tk

class MovingObject:
    def __init__(self, canvas, cell_size):
        self.canvas = canvas
        self.cell_size = cell_size
        self.obj = self.canvas.create_rectangle(0, 0, cell_size, cell_size, fill='blue')
        self.canvas.bind('<Button-1>', self.move)

    def move(self, event):
        x, y = event.x, event.y
        col = x // self.cell_size
        row = y // self.cell_size
        self.canvas.coords(self.obj, col*self.cell_size, row*self.cell_size, col*self.cell_size+self.cell_size, row*self.cell_size+self.cell_size)
        self.canvas.coords()
class MainApp:
    def __init__(self, root, rows, columns, cell_size):
        self.root = root
        self.canvas = tk.Canvas(root, width=columns*cell_size, height=rows*cell_size)
        self.canvas.pack()
        self.moving_obj = MovingObject(self.canvas, cell_size)

if __name__ == '__main__':
    rows = 5
    columns = 5
    cell_size = 50

    root = tk.Tk()
    app = MainApp(root, rows, columns, cell_size)

    root.mainloop()
