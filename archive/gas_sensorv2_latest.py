# Created by TheGullibleKid at 8/09/2021
# @author: mumble-07

import board
import busio
import math
from math import pow, log, exp
import time
from time import sleep,strftime
from datetime import datetime
import os
import glob
import time
import numpy as np
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

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
iteration = 5 #times
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

#================= SENSOR CURVES =================

def gas_percentage (rs, ro, gas_type, ro_factor):
    
    ro_prime = ro * math.exp(math.log(gas_type[0]/ro_factor)/gas_type[1])
    ppm = gas_type[0] * pow((rs/ro_prime), gas_type[1])
    
    
    return ppm

while True:
    
    Rs_read_2600 = rs_read_sensor (TGS_2600, Vc, RL_2600, time_interval, iteration)
    Rs_read_2602 = rs_read_sensor (TGS_2602, Vc, RL_2602, time_interval, iteration)
    Rs_read_2611 = rs_read_sensor (TGS_2611, Vc, RL_2611, time_interval, iteration)
    Rs_read_2620 = rs_read_sensor (TGS_2620, Vc, RL_2620, time_interval, iteration)

    
    ppm_CO = gas_percentage (Rs_read_2600, Ro_2600, gas_CO, Ro_factor_2600)
    ppm_toulene = gas_percentage (Rs_read_2602, Ro_2602, gas_toulene, Ro_factor_2602)
    ppm_ammonia = gas_percentage (Rs_read_2602, Ro_2602, gas_ammonia, Ro_factor_2602)
    ppm_methane = gas_percentage (Rs_read_2611, Ro_2611, gas_methane, Ro_factor_2611)
    ppm_ethanol = gas_percentage (Rs_read_2620, Ro_2620, gas_ethanol, Ro_factor_2620)
    print ("CO: ", ppm_CO, "Toulene: ", ppm_toulene, "Ammonia: ", ppm_ammonia, "Methane: ", ppm_methane, "Ethanol: ", ppm_ethanol)
    sleep(0.5)