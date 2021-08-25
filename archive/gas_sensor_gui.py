# /*
#  * @Author: andy.mumble-07 
#  * @Date: 2021-08-11 06:32:49 
#  * @Last Modified by:   andy.mumble-07 
#  * @Last Modified time: 2021-08-11 06:32:49 
#  */
# Created by TheGullibleKid at 7/27/2021
# @author: mumble-07

from tkinter import *

#root as the main GUI window

root =Tk()
root.title("Gas Sensor GUI")
root.geometry("500x300")

windowTitle = Label(root, text="IED E-Nose System", fg='red', font=('calibri', 30)).grid(row=0, column=2)

#GAS LEVEL
GASLEVEL = Label(root, text="GAS LEVEL: ", fg="green", font=('calibri', 20))
GASLEVEL.grid(row=1, column=1)

STATUS = Label(root, text="SAFE", fg="green", font=('calibri', 20))
STATUS.grid(row=2, column=1)

#GAS TYPE
KCL = Label(root, text="Potassium Chloride (KCL)", fg='blue', font=('calibri', 12))
KCL.grid(row=1, column=2)
Sulfur = Label(root, text="Sulfur(S)", fg='blue', font=('calibri', 12))
Sulfur.grid(row=2, column=2)
ANitrate = Label(root, text="Ammonium Nitrate (NH4NO3)", fg='blue', font=('calibri', 12))
ANitrate.grid(row=3, column=2)
Acetone = Label(root, text="Acetone (C3H6O)", fg='blue', font=('calibri', 12))
Acetone.grid(row=4, column=2)
HPeroxide=Label(root, text="Hydrogen Peroxide (H2O2)", fg='blue', font=('calibri', 12))
HPeroxide.grid(row=5, column=2)

#GAS LEVELS
GL_KCL = Label(root, text="0%", fg='blue', font=('calibri', 12))
GL_KCL.grid(row=1, column=3)
GL_Sulfur = Label(root, text="0%", fg='blue', font=('calibri', 12))
GL_Sulfur.grid(row=2, column=3)
GL_ANitrate = Label(root, text="0%", fg='blue', font=('calibri', 12))
GL_ANitrate.grid(row=3, column=3)
GL_Acetone = Label(root, text="0%", fg='blue', font=('calibri', 12))
GL_Acetone.grid(row=4, column=3)
GL_HPeroxide=Label(root, text="0%", fg='blue', font=('calibri', 12))
GL_HPeroxide.grid(row=5, column=3)
#windowTitle.pack()
#had issues of multiple lines (ALWAYS REFACTOR NALANG!)

#Function Button of Force Refresh - parang reset button function
def Reset_on_Click():
    print("Force Refresh")

#Button Force Refresh
forceRefreshbtn = Button(root, width=20, borderwidth=5, height= 2, text="Force Refresh", command= Reset_on_Click, fg="black", font=('calibri', 10), bg="yellow")
forceRefreshbtn.grid(row=7, column=2)

def close_window():
  root.destroy()
  print( "Window closed")


#for clean up exit
root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()