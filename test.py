import tkinter as tk


def select_image(event):
    # Определяем координаты курсора при нажатии
    x, y = event.x, event.y

    # Определяем объекты, находящиеся под курсором
    items = canvas.find_overlapping(x, y, x, y)

    if len(items) > 0:
        # Выделяем первый найденный объект рамкой
        canvas.itemconfig(items[0], outline='red', width=2)


def deselect_image(event):
    # Определяем объекты на холсте и убираем рамку у всех изображений
    items = canvas.find_all()
    for item in items:
        canvas.itemconfig(item, outline='black', width=1)


root = tk.Tk()

canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Загружаем изображение
image = tk.PhotoImage(file="image/ball.png")

# Создаем изображение на холсте
image_id = canvas.create_image(100, 100, image=image, anchor=tk.NW)

# Привязываем обработчики событий для нажатия и отпускания кнопки мыши
canvas.bind('<Button-1>', select_image)
canvas.bind('<ButtonRelease-1>', deselect_image)

root.mainloop()
