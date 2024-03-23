import tkinter as tk

def format_time(seconds):
    minutes, sec = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02d}:{:02d}:{:02d}".format(hours, minutes, sec)

def update_countdown():
    global countdown
    if countdown > 0:
        time_str = format_time(countdown)
        label.config(text=time_str)
        countdown -= 1
        label.after(1000, update_countdown)
    else:
        label.config(text="Время вышло!")

root = tk.Tk()
root.title("Обратный отсчет")

countdown = 3600  # начальное значение времени для обратного отсчета (3600 секунд = 1 час)

label = tk.Label(root, font=("Helvetica", 24))
label.pack()

update_countdown()

root.mainloop()