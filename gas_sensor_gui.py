# Created by TheGullibleKid at 7/27/2021
# @author: mumble-07

from tkinter import *

root =Tk()
root.title("Gas Sensor GUI")
root.geometry("500x300")

windowTitle = Label(root, text="IED E-Nose System").grid(row=0, column=1)
#windowTitle.pack()
#Text Inputs
#had issues of multiple lines (ALWAYS REFACTOR!!!)
testTry = Entry(root, width=50, borderwidth=5)
testTry.grid(row=1, column=2)

def on_Click():
    print(f" {testTry.get()}")
#Buttons

forceRefreshbtn = Button(root, text="Force Refresh", command= on_Click).grid(row=2, column=1)

root.mainloop()