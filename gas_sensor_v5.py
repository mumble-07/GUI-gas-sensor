# Created by TheGullibleKid at 8/09/2021
# @author: mumble-07

from tkinter import *
import csv
import board
import busio
import math
from math import pow
from time import sleep, strftime
from datetime import datetime
import numpy as np
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
from firebase import firebase

i2c =busio.I2C(board.SCL,board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads,ADS.P0)

Ro_Value = np.loadtxt("/home/pi/Desktop/Ro_values.csv", delimiter=",")
print("New file", Ro_Value)

TGS_2600 = 1 #use to declare sensor type
TGS_2602 = 2 
TGS_2611 = 3
TGS_2620 = 4
#================= Constants =================
Vc = 5 #volts from data sheet
time_interval = .1 #in secs
iteration = 10 #times
Calib_time_interval = .1 #in secs
Calib_iteration = 10 #times
#================= TGS-2600 Definition =================
RL_2600 = 20000 #in ohm RL min
Ro_2600 = Ro_Value[0] #in Ohm
Ro_factor_2600 = 1
gas_CO = np.array([1.144997421, -0.21687423], dtype=float)
#================= TGS-2602 Definition =================
RL_2602 = 4700 #in ohm RL min
Ro_2602 = Ro_Value[1] #in Ohm
Ro_factor_2602 = 1
gas_toluene = np.array([0.163063, -1.63343], dtype=float)
gas_ammonia = np.array([0.93178, -3.10356], dtype=float)
#================= TGS-2611 Definition =================
RL_2611 = 4700 #in ohm RL min
Ro_2611 = Ro_Value[2] #in Ohm
Ro_factor_2611 = 9
gas_methane = np.array([5090.43, -2.26059], dtype=float)
gas_isobutane = np.array([24919.3, -2.72606], dtype=float) #Add data here later
#================= TGS-2620 Definition =================
RL_2620 = 4700 #in ohm RL min
Ro_2620 = Ro_Value[3] #in Ohm
Ro_factor_2620 = 20
gas_ethanol = np.array([321.229, -1.57881], dtype=float)
#================= Functions =================

#================= RO CALIBRATION =================
def Calibration_sensor_read():
    Ro_read= np.array([0,0,0,0],dtype=float)
    Ro_read[0] = rs_read_sensor (TGS_2600, Vc, RL_2600, Calib_time_interval, Calib_iteration) #Rs_read_2600
    Ro_read[1] = rs_read_sensor (TGS_2602, Vc, RL_2602, Calib_time_interval, Calib_iteration) #Rs_read_2602
    Ro_read[2] = rs_read_sensor (TGS_2611, Vc, RL_2611, Calib_time_interval, Calib_iteration) #Rs_read_2611
    Ro_read[3] = rs_read_sensor (TGS_2620, Vc, RL_2620, Calib_time_interval, Calib_iteration) #Rs_read_2620
    np.savetxt("/home/pi/Desktop/Ro_values.csv", Ro_read, delimiter=",")
    Ro_Value = np.loadtxt("/home/pi/Desktop/gas_/Ro_values.csv", delimiter=",")
    print("New Ro Values", Ro_Value)

#================= RS CALCULATION =================
def sensor_read():
    Rs_read= np.array([0,0,0,0],dtype=float)
    Rs_read[0] = rs_read_sensor (TGS_2600, Vc, RL_2600, time_interval, iteration) #Rs_read_2600
    Rs_read[1] = rs_read_sensor (TGS_2602, Vc, RL_2602, time_interval, iteration) #Rs_read_2602
    Rs_read[2] = rs_read_sensor (TGS_2611, Vc, RL_2611, time_interval, iteration) #Rs_read_2611
    Rs_read[3] = rs_read_sensor (TGS_2620, Vc, RL_2620, time_interval, iteration) #Rs_read_2620
    return Rs_read


def rs_read_sensor (gaspin, sv, rl, ti, times):
    Rs_sum = 0
    i_times = 0
    while times > i_times:
         if gaspin == 1:
            tgs_value = AnalogIn(ads,ADS.P0)
         elif gaspin == 2:
           tgs_value = AnalogIn(ads,ADS.P1)
         elif gaspin ==3:
           tgs_value = AnalogIn(ads,ADS.P2)
         elif gaspin == 4:
           tgs_value = AnalogIn(ads,ADS.P3)        
        
         Rs = ((sv*rl)/((tgs_value.value * sv) / 37750))-rl
         Rs_sum = Rs_sum + Rs
         sleep(ti)
         i_times = i_times + 1
    #print (Rs," ", Rs_sum)
 
    Ave_Rs = Rs_sum/times
  
    return Ave_Rs

def v_read_sensor (RSarray, sv):
    rs = RSarray
      
    Ave_volts = np.array([0,0,0,0],dtype=float)  
    Ave_volts[0]  = (sv*20000)/(RSarray[0]+20000)
    Ave_volts[1]  = (sv*4700)/(RSarray[1]+4700)
    Ave_volts[2]  = (sv*4700)/(RSarray[2]+4700)
    Ave_volts[3]  = (sv*4700)/(RSarray[3]+4700)
    
  
    return Ave_volts

#================= SENSOR CURVES =================
def gas_ppm (rs, ro, gas_type, ro_factor):
    
    ro_prime = ro * math.exp(math.log(gas_type[0]/ro_factor)/gas_type[1])
    ppm = gas_type[0] * pow((rs/ro_prime), gas_type[1])
    
    
    return ppm

def gas_write():
    Rs_read_value = sensor_read()
    ppm_gas= np.array([0,0,0,0,0,0],dtype=float, )
    ppm_gas[0]= gas_ppm (Rs_read_value[0], Ro_2600, gas_CO, Ro_factor_2600)
    ppm_gas[1] = gas_ppm (Rs_read_value[1], Ro_2602, gas_toluene, Ro_factor_2602)
    ppm_gas[2] = gas_ppm (Rs_read_value[1], Ro_2602, gas_ammonia, Ro_factor_2602)
    ppm_gas[3] = gas_ppm (Rs_read_value[2], Ro_2611, gas_methane, Ro_factor_2611)
    ppm_gas[5] = gas_ppm (Rs_read_value[2], Ro_2611, gas_isobutane, Ro_factor_2611)
    ppm_gas[4] = gas_ppm (Rs_read_value[3], Ro_2620, gas_ethanol, Ro_factor_2620)
    return np.around(ppm_gas, 3)


def csv_log(gas_array):

    ppm_gasarray = np.array([0,0,0,0,0,0],dtype=float )
    ppm_gasarray = gas_array

    if ppm_gasarray[0] is not None and ppm_gasarray[1] is not None and ppm_gasarray[2] is not None and ppm_gasarray[3] is not None and ppm_gasarray[4] is not None and ppm_gasarray[5] is not None:
        log = open("/home/pi/Desktop/log.csv","a")  
        log.write("PPM" +" , " + "{0:0.3f}".format(ppm_gasarray[0]) +" , " + "{0:0.3f}".format(ppm_gasarray[1]) + " , "+ "{0:0.3f}".format(ppm_gasarray[2])+ " , "+ "{0:0.3f}".format(ppm_gasarray[3])+ " , "+ "{0:0.3f}".format(ppm_gasarray[4])+ " , " + "{0:0.3f}".format(ppm_gasarray[5])+ " , ")
        
    else:
        log =open("/home/pi/Desktop/log.csv","a") 
        log.write("NAN   "+ ",")
        
    log.write(datetime.today().strftime("%m-%d-%Y %H:%M:%S")+ "\n")
    log.close()
    sleep(0.1)

# GUI FUNCTIONS


def close_window():
    root.destroy()
    print( "Window closed")

def screen_display():
    rs = sensor_read()
    ppm_gasarray= gas_write()
    volts= v_read_sensor(rs,Vc)
    
    raw_CO = ppm_gasarray[0]
    raw_Toluene = ppm_gasarray[1]
    raw_Ammonia = ppm_gasarray[2]
    raw_Methane = ppm_gasarray[3]
    raw_Ethanol = ppm_gasarray[4]
    raw_Isobutane = ppm_gasarray[5]
    
    print ("CO: ", raw_CO, "toluene: ", raw_Toluene, "Ammonia: ", raw_Ammonia, "Methane: ", raw_Methane, "Ethanol: ", raw_Ethanol, "Isobutane: ", raw_Isobutane)

    GL_CO = Label(root, text= raw_CO, fg='blue', font=('calibri', 12), anchor='center')
    GL_CO.grid(row=1, column=3)
    GL_Toluene = Label(root, text= raw_Toluene, fg='blue', font=('calibri', 12), anchor='center')
    GL_Toluene.grid(row=2, column=3)
    GL_Ammonia = Label(root, text= raw_Ammonia, fg='blue', font=('calibri', 12), anchor='center')
    GL_Ammonia.grid(row=3, column=3)
    GL_Methane = Label(root, text= raw_Methane, fg='blue', font=('calibri', 12), anchor='center')
    GL_Methane.grid(row=4, column=3)
    GL_Ethanol=Label(root, text= raw_Ethanol, fg='blue', font=('calibri', 12), anchor='center')
    GL_Ethanol.grid(row=5, column=3)
    GL_Isobutane=Label(root, text= raw_Isobutane, fg='blue', font=('calibri', 12), anchor='center')
    GL_Isobutane.grid(row=6, column=3)
    
    forceRefreshbtn = Button(root, width=20, borderwidth=5, height= 2, text="CALIBRATION", command= Calibration_sensor_read, fg="black", font=('calibri', 10), bg="yellow")
    forceRefreshbtn.grid(row=8, column=2)
    
    #==========FIREBASE==========================
    
    firebase_data = firebase.FirebaseApplication("https://gassensor-db-default-rtdb.firebaseio.com/", None)
    
    
    
    data = {
        'Ammonia': raw_Ammonia,
        'CO': raw_CO,
        'Ethanol': raw_Ethanol,
        'Isobutane': raw_Isobutane,
        'Methane': raw_Methane,
        'Toluene': raw_Toluene,
        'H_Timestamp': datetime.today().strftime("%H"),
        'M_Timestamp': datetime.today().strftime("%M"),
        'Gas_Status': 0
            }
    
    result = firebase_data.put('/gassensor-db-default-rtdb/gasdata:',"-MhvYPVvC3476qBwCADx", data)
    print(result)

     #=============LOG==============   

    # if ppm_gasarray[0] is not None and ppm_gasarray[1] is not None and ppm_gasarray[2] is not None and ppm_gasarray[3] is not None and ppm_gasarray[4] is not None and ppm_gasarray[5] is not None:
    #     log = open("/home/pi/Desktop/log.csv","a")  
    #     log.write("V" + " , " +"{0:0.3f}".format(volts[0]) +" , "+"{0:0.3f}".format(volts[1]) +" , "+"{0:0.3f}".format(volts[2]) +" , "+"{0:0.3f}".format(volts[3]) +" , " +"RS" + " , " +"{0:0.3f}".format(rs[0]) +" , "+"{0:0.3f}".format(rs[1]) +" , "+"{0:0.3f}".format(rs[2]) +" , "+"{0:0.3f}".format(rs[3]) +" , " + "PPM" +" , " + "{0:0.3f}".format(ppm_gasarray[0]) +" , " + "{0:0.3f}".format(ppm_gasarray[1]) + " , "+ "{0:0.3f}".format(ppm_gasarray[2])+ " , "+ "{0:0.3f}".format(ppm_gasarray[3])+ " , "+ "{0:0.3f}".format(ppm_gasarray[4])+ " , " + "{0:0.3f}".format(ppm_gasarray[5])+ " , ")
            
    # else:
    #     log =open("/home/pi/Desktop/log.csv","a") 
    #     log.write("NAN   "+ ",")
            
    # log.write(datetime.today().strftime("%m-%d-%Y %H:%M:%S")+ "\n")
    # log.close()
    # sleep(0.1)

    csv_log(ppm_gasarray)
    
    GL_CO.after(100, screen_display)
    
root = Tk()
root.title("Gas Sensor GUI")
root.geometry("480x320")

windowTitle = Label(root, text="IED E-Nose System", fg='red', font=('calibri', 30), anchor ="center").grid(row=0, column=2, columnspan=2)


GASLEVEL = Label(root, text="GAS LEVEL: ", fg="green", font=('calibri', 20))
GASLEVEL.grid(row=7, column=2)

STATUS = Label(root, text="SAFE", fg="green", font=('calibri', 20))
STATUS.grid(row=7, column=3)
#GAS TYPE

CO = Label(root, text="Carbon Monoxide (CO)", fg='blue', font=('calibri', 12)).grid(row=1, column=2)
toluene = Label(root, text="toluene", fg='blue', font=('calibri', 12)).grid(row=2, column=2)
Ammonia = Label(root, text="Ammonia", fg='blue', font=('calibri', 12)).grid(row=3, column=2)
Methane = Label(root, text="Methane", fg='blue', font=('calibri', 12)).grid(row=4, column=2)
Ethanol=Label(root, text="Ethanol", fg='blue', font=('calibri', 12)).grid(row=5, column=2)
Isobutane=Label(root, text="Isobutane", fg='blue', font=('calibri', 12)).grid(row=6, column=2)


GL_CO = Label(root, text= 0, fg='blue', font=('calibri', 12))
GL_CO.grid(row=1, column=3)
GL_toluene = Label(root, text= 0, fg='blue', font=('calibri', 12)).grid(row=2, column=3)
GL_Ammonia = Label(root, text= 0, fg='blue', font=('calibri', 12)).grid(row=3, column=3)
GL_Methane = Label(root, text= 0, fg='blue', font=('calibri', 12)).grid(row=4, column=3)
GL_Ethanol=Label(root, text= 0, fg='blue', font=('calibri', 12)).grid(row=5, column=3)
GL_Isobutane=Label(root, text= 0, fg='blue', font=('calibri', 12)).grid(row=6, column=3)
GL_CO.after(500, screen_display)
        
#for clean up exit
root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()

