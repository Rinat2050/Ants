## ООП автосалон
# TODO: обозначения координат на доске chess_field = Frame()
# TODO: возможность отключения подцветки для коня Checkbutton
# TODO: убрать зелёные после победы

from tkinter import *
from pprint import pprint
from tkinter.messagebox import askquestion
from tkinter import ttk

# tkinter обрабатывает события

count = 0  # глобальная переменная для счетчика ходов


def click(M, row, column):  # функция клика по кнопке
    global count  # делаем переменную видимой для функции click
    if valid_step(M, row, column):
        x, y = search_K(M)
        M[x][y] = ' '
        M[row][column] = 'K'
        count += 1
        update_window(M)
        color_valid_step(M, list_of_button)
        lbl_count.config(text=f'Ходов: {count}')
        if check_win(M):
            askquestion(title="УРА !!!", message=f'Победа! \nВы победили за {count} ходов')
            M[0][0] = 'K'
            M[7][7] = ' '
            count = 0
            lbl_count.config(text=f'Ходов: {count}')
            update_window(M)
            color_valid_step(M, list_of_button)
    else:
        lbl_error_step.grid_forget()
        lbl_error_step.grid(row=2, column=8)


def color_valid_step(M, list):  # функция окрашивания кнопок для возможного хода
    # print(enabled.get())
    for i in range(len(M)):
        for j in range(len(M[i])):
            if valid_step(M, i, j):
                list_in_matrix(list)[i][j].configure(bg='green')
            else:
                if (i + j) % 2 == 0:
                    list_in_matrix(list)[i][j].configure(bg='white')
                else:
                    list_in_matrix(list)[i][j].configure(bg='gray')


def update_window(M):  # функция обновления окна
    for i in range(len(M)):
        for j in range(len(M[i])):
            list_in_matrix(list_of_button)[i][j].configure(text=M[i][j])


def search_K(M):  # функция ищет и возвращает координаты К
    for row in range(len(M)):
        for column in range(len(M[row])):
            if M[row][column] == 'K':
                return row, column


def list_in_matrix(list):  # функция перобразует список в матрицу
    res = []
    sub = []
    for i in range(len(list)):
        sub.append(list[i])
        if (i + 1) % 8 == 0:
            res.append(sub)
            sub = []
    return res


def valid_step(M, x2, y2):  # функция проверяет возможность хода
    x1, y1 = search_K(M)
    if abs(x2 - x1) == 1 and abs(y2 - y1) == 2 or abs(x2 - x1) == 2 and abs(y2 - y1) == 1:
        return True
    else:
        return False


def check_win(M):  # функция проверяет победу
    if search_K(M) == (7, 7):
        return True
    else:
        return False


def checkbutton_changed():
    pass
    # print(enabled.get())


window = Tk()
window.title("Конь")
window.geometry('530x500')

M = []
for _ in range(8):
    sub_M = []
    for j in range(8):
        sub_M.append(' ')
    M.append(sub_M)

M[0][0] = 'K'
# pprint(M)

list_of_button = []  # список кнопок
chess_field = Frame(window)  # метод создания рамки
chess_field.grid(row=2, column=0)

param_field = Frame(window)
param_field.grid(row=2, column=3)

x1_field = Frame(window)
x1_field.grid(row=0, column=0)
alfa = 'abcdefgh'
for i in range(8):
    lable_x1 = Label(x1_field, text=alfa[i], width=6, height=1)
    lable_x1.grid(row=0, column=i)
    lable_x1.grid(row=3, column=i)

y1_field = Frame()
y1_field.grid(row=2, column=0)

for row in range(8):
    for column in range(8):
        if (row + column) % 2 == 0:
            color = 'white'
        else:
            color = 'gray'
        btn = Button(chess_field, text=(M[row][column]),
                     width=3, height=3, bg=color,
                     command=lambda M=M, row=row, column=column: click(M, row,
                                                                       column))  # lambda - анонимная функция что передает лямбда в функцию click
        btn.grid(row=row, column=column)  # размещение кнопки в окне
        list_of_button.append(btn)
color_valid_step(M, list_of_button)

# создание счетчика ходов
lbl_count = Label(param_field, text=f'Ходов: {count}')
lbl_count.config(width=10, height=1)
lbl_count.grid(row=0, column=8)

# создание кнопки для включения подсветки
enabled = IntVar()
checkbutton = ttk.Checkbutton(param_field, text="Подсветка", variable=enabled, command=checkbutton_changed)
checkbutton.grid(row=1, column=8)

# вывод текста "Неверный ход"
lbl_error_step = Label(param_field, text='Неверный\nход', fg='red')
lbl_error_step.config(width=10, height=2)

window.mainloop()
