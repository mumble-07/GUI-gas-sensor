# Created by Inevitably Lefty at 7/26/2021
# @author: TheGullibleKid

from tkinter import *

main_window = Tk()

#Labels

Label(main_window, text="Gas Sensor App").grid(row=0, column=1)
Label(main_window, text="TKINTER").grid(row= 1, column=1)


#Text Inputs
#had issues of multiple lines (ALWAYS REFACTOR!!!)
gas_sensor = Entry(main_window, width=50, borderwidth=5)
gas_sensor.grid(row=0, column=2)
testTry = Entry(main_window, width=50, borderwidth=5)
testTry.grid(row=1, column=2)


def on_Click():
    print(f"{gas_sensor.get()}, {testTry.get()}")
#Buttons

Button(main_window, text="Send", command= on_Click).grid(row=2, column=1)


main_window.mainloop()