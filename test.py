import tkinter as tk

def select_shape(event):
    global selected_shape
    x, y = event.x, event.y
    if circle_coords[0] <= x <= circle_coords[2] and circle_coords[1] <= y <= circle_coords[3]:
        canvas.itemconfig(circle, outline='red')
        canvas.itemconfig(square, outline='')
        selected_shape = 'circle'
    elif square_coords[0] <= x <= square_coords[2] and square_coords[1] <= y <= square_coords[3]:
        canvas.itemconfig(square, outline='red')
        canvas.itemconfig(circle, outline='')
        selected_shape = 'square'

def move_shape(event):
    global selected_shape
    if selected_shape == 'circle':
        canvas.coords(circle, event.x - 25, event.y - 25, event.x + 25, event.y + 25)
    elif selected_shape == 'square':
        canvas.coords(square, event.x - 25, event.y - 25, event.x + 25, event.y + 25)

root = tk.Tk()
root.title('Select and Move Shapes')

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

circle = canvas.create_oval(150, 150, 250, 250, outline='black', width=2)
square = canvas.create_rectangle(50, 50, 100, 100, outline='black', width=2)

circle_coords = canvas.coords(circle)
square_coords = canvas.coords(square)

selected_shape = None

canvas.bind('<Button-1>', select_shape)
canvas.bind('<B1-Motion>', move_shape)

root.mainloop()
