import tkinter as tk

def on_label_click(event):
    label = event.widget
    print(f"Clicked: {label['text']}")


root = tk.Tk()

label1 = tk.Label(root, text="Label 1", bg="red")
label1.pack()

label2 = tk.Label(root, text="Label 2", bg="blue")
label2.pack()

def propagate_click(event):
    event.widget.event_generate("<Button-1>", x=event.x, y=event.y)

label1.bind("<Button-1>", propagate_click)
label2.bind("<Button-1>", on_label_click)

root.mainloop()
