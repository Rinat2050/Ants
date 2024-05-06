from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo

root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")


def open_warning():
    showwarning(title="Предупреждение", message="Игра окончилась")


warning_button = ttk.Button(text="Предупреждение", command=open_warning)
warning_button.pack(anchor="center", expand=1)

root.mainloop()