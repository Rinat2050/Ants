from tkinter import *
from tkinter import ttk

root = Tk()
root.title("METANIT.COM")
root.geometry("250x150")

progressbar = ttk.Progressbar(orient="horizontal", mode="indeterminate")
progressbar.pack(fill=X, padx=10, pady=10)

start_btn = ttk.Button(text="Start", command=progressbar.start)
start_btn.pack(anchor=SW, side=LEFT, padx=10, pady=10)

stop_btn = ttk.Button(text="Stop", command=progressbar.stop)
stop_btn.pack(anchor=SE, side=RIGHT, padx=10, pady=10)

root.mainloop()