import tkinter as tk
from tkinter import ttk
import time

def start_progress():
    progressbar_indeterminate.start(10)
    time.sleep(2)
    progressbar_indeterminate.stop()

    for i in range(101):
        time.sleep(0.05)
        progress_var.set(i)
        root.update_idletasks()

root = tk.Tk()
root.title("Progressbar Example")
root.geometry("300x150")

progress_var = tk.DoubleVar()
progressbar_determinate = ttk.Progressbar(
    root,
    variable=progress_var,
    orient="horizontal",
    length=200,
    mode="determinate"
)
progressbar_determinate.pack(pady=20)

progressbar_indeterminate = ttk.Progressbar(
    root,
    orient="horizontal",
    length=200,
    mode="indeterminate"
)
progressbar_indeterminate.pack(pady=20)

start_button = tk.Button(root, text="Start Progress", command=start_progress)
start_button.pack(pady=10)

root.mainloop()