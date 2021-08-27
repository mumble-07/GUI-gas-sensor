# Created by TheGullibleKid at 8/09/2021
# @author: mumble-07

from tkinter import *
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


TGS_2600 = 1 #use to declare sensor type
TGS_2602 = 2 
TGS_2611 = 3
TGS_2620 = 4
#================= Constants =================
Vc = 5 #volts from data sheet
time_interval = .1 #in secs
iteration = 10 #times
#================= TGS-2600 Definition =================
RL_2600 = 20000 #in ohm RL min
Ro_2600 = 50600 #in Ohm
Ro_factor_2600 = 1
gas_CO = np.array([1.144997421, -0.21687423], dtype=float)
#================= TGS-2602 Definition =================
RL_2602 = 4700 #in ohm RL min
Ro_2602 = 5040 #in Ohm
Ro_factor_2602 = 1
gas_toulene = np.array([0.163063, -1.63343], dtype=float)
gas_ammonia = np.array([0.93178, -3.10356], dtype=float)
#================= TGS-2611 Definition =================
RL_2611 = 4700 #in ohm RL min
Ro_2611 = 18200 #in Ohm
Ro_factor_2611 = 9
gas_methane = np.array([5090.43, -2.26059], dtype=float)
#================= TGS-2620 Definition =================
RL_2620 = 4700 #in ohm RL min
Ro_2620 = 8500 #in Ohm
Ro_factor_2620 = 20
gas_ethanol = np.array([321.229, -1.57881], dtype=float)
#================= Functions =================

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
    ppm_gas= np.array([0,0,0,0,0],dtype=float, )
    ppm_gas[0]= gas_ppm (Rs_read_value[0], Ro_2600, gas_CO, Ro_factor_2600)
    ppm_gas[1] = gas_ppm (Rs_read_value[1], Ro_2602, gas_toulene, Ro_factor_2602)
    ppm_gas[2] = gas_ppm (Rs_read_value[1], Ro_2602, gas_ammonia, Ro_factor_2602)
    ppm_gas[3] = gas_ppm (Rs_read_value[2], Ro_2611, gas_methane, Ro_factor_2611)
    ppm_gas[4] = gas_ppm (Rs_read_value[3], Ro_2620, gas_ethanol, Ro_factor_2620)
    return np.around(ppm_gas, 3)


# GUI FUNCTIONS

def Reset_on_Click():
    gas_write()
    print("Force Refresh")


def close_window():
    root.destroy()
    print( "Window closed")

def screen_display():
    rs = sensor_read()
    ppm_gasarray= gas_write()
    volts= v_read_sensor(rs,Vc)
    
    raw_CO = ppm_gasarray[0]
    raw_Toulene = ppm_gasarray[1]
    raw_Ammonia = ppm_gasarray[2]
    raw_Methane = ppm_gasarray[3]
    raw_Ethanol = ppm_gasarray[4]
    
    print ("CO: ", raw_CO, "Toulene: ", raw_Toulene, "Ammonia: ", raw_Ammonia, "Methane: ", raw_Methane, "Ethanol: ", raw_Ethanol)

    GL_CO = Label(root, text= raw_CO, fg='blue', font=('calibri', 12), anchor='center')
    GL_CO.grid(row=1, column=3)
    GL_Toulene = Label(root, text= raw_Toulene, fg='blue', font=('calibri', 12), anchor='center')
    GL_Toulene.grid(row=2, column=3)
    GL_Ammonia = Label(root, text= raw_Ammonia, fg='blue', font=('calibri', 12), anchor='center')
    GL_Ammonia.grid(row=3, column=3)
    GL_Methane = Label(root, text= raw_Methane, fg='blue', font=('calibri', 12), anchor='center')
    GL_Methane.grid(row=4, column=3)
    GL_Ethanol=Label(root, text= raw_Ethanol, fg='blue', font=('calibri', 12), anchor='center')
    GL_Ethanol.grid(row=5, column=3)
    
    
    firebase_data = firebase.FirebaseApplication("https://gassensor-db-default-rtdb.firebaseio.com/", None)

    data = {
        'Ammonia': raw_Ammonia,
        'CO': raw_CO,
        'Ethanol': raw_Ethanol,
        'Methane': raw_Methane,
        'Toulene': raw_Toulene,
        'X_Timestamp': datetime.today().strftime("%m-%d-%Y %H:%M:%S")
            }

    result = firebase_data.post('/gassensor-db-default-rtdb/gasdata:', data)
    print(result)
    get_result = firebase_data.get('/gassensor-db-default-rtdb/gasdata:', '')
    print(get_result)
    
    if ppm_gasarray[0] is not None and ppm_gasarray[1] is not None and ppm_gasarray[2] is not None and ppm_gasarray[3] is not None:
        log = open("/home/pi/Desktop/log.csv","a")  
        log.write("V" + " , " +"{0:0.3f}".format(volts[0]) +" , "+"{0:0.3f}".format(volts[1]) +" , "+"{0:0.3f}".format(volts[2]) +" , "+"{0:0.3f}".format(volts[3]) +" , " +"RS" + " , " +"{0:0.3f}".format(rs[0]) +" , "+"{0:0.3f}".format(rs[1]) +" , "+"{0:0.3f}".format(rs[2]) +" , "+"{0:0.3f}".format(rs[3]) +" , " + "PPM" +" , " + "{0:0.3f}".format(ppm_gasarray[0]) +" , " + "{0:0.3f}".format(ppm_gasarray[1]) + " , "+ "{0:0.3f}".format(ppm_gasarray[2])+ " , "+ "{0:0.3f}".format(ppm_gasarray[3])+ " , "+ "{0:0.3f}".format(ppm_gasarray[4])+ " , ")
            
    else:
        log =open("/home/pi/Desktop/log.csv","a") 
        log.write("NAN   "+ ",")
            
    log.write(datetime.today().strftime("%m-%d-%Y %H:%M:%S")+ "\n")
    log.close()
    sleep(0.1)
    
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
Toulene = Label(root, text="Toulene", fg='blue', font=('calibri', 12)).grid(row=2, column=2)
Ammonia = Label(root, text="Ammonia", fg='blue', font=('calibri', 12)).grid(row=3, column=2)
Methane = Label(root, text="Methane", fg='blue', font=('calibri', 12)).grid(row=4, column=2)
Ethanol=Label(root, text="Ethanol", fg='blue', font=('calibri', 12)).grid(row=5, column=2)


GL_CO = Label(root, text= 0, fg='blue', font=('calibri', 12))
GL_CO.grid(row=1, column=3)
GL_Toulene = Label(root, text= 0, fg='blue', font=('calibri', 12)).grid(row=2, column=3)
GL_Ammonia = Label(root, text= 0, fg='blue', font=('calibri', 12)).grid(row=3, column=3)
GL_Methane = Label(root, text= 0, fg='blue', font=('calibri', 12)).grid(row=4, column=3)
GL_Ethanol=Label(root, text= 0, fg='blue', font=('calibri', 12)).grid(row=5, column=3)
GL_CO.after(500, screen_display)
    
#for clean up exit
root.protocol("WM_DELETE_WINDOW", close_window)
root.mainloop()    

   
   