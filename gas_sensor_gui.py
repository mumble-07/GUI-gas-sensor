# Created by TheGullibleKid at 7/27/2021
# @author: mumble-07

from tkinter import *

#root as the main GUI window

root =Tk()
root.title("Gas Sensor GUI")
root.geometry("500x300")

windowTitle = Label(root, text="IED E-Nose System", fg='red', font=('calibri', 30)).grid(row=0, column=2)

#HEADER
Label(root, text="GAS LEVEL: ", fg="green", font=("calibri", 15)).grid(row=1, column=1)

#GAS LEVEL
Label(root, text="SAFE", fg="green", font=("calibri", 15)).grid(row=2, column=1)

#windowTitle.pack()
#had issues of multiple lines (ALWAYS REFACTOR NALANG!)

#Function Button of Force Refresh
def on_Click():
    print("Force Refresh")

#Button Force Refresh
forceRefreshbtn = Button(root, text="Force Refresh", command= on_Click, fg="green", bg="yellow").grid(row=5, column=3)





root.mainloop()