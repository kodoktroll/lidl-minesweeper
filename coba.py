from tkinter import *
from tkinter import filedialog
from tkinter.ttk import *
import tkinter.messagebox

root = Tk()

tkinter.Label(root, text="Choose:").grid(row=1, column=1, sticky=W)
var3 = IntVar(value=1)

entry = tkinter.Entry(root,  width="10")
entry.insert(10, 'Text')
entry.grid(row=5, column=4, sticky=W)
entry.configure(state='disabled')

def naccheck(entry, var3):
    if var3.get() != 2:
        entry.configure(state='disabled')
    else:
        entry.configure(state='normal')

rbtn1 = Radiobutton(root, text="Option 1", variable=var3, value=1,command=lambda e=entry, v=var3: naccheck(e,v))
rbtn1.grid(row=1, column=2, sticky=W)

rbtn2 = Radiobutton(root, text="Option 2", variable=var3, value=2, command=lambda e=entry, v=var3: naccheck(e,v))
rbtn2.grid(row=5, column=2, sticky=E)

root.mainloop()