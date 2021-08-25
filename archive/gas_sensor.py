# Created by TheGullibleKid at 8/09/2021
# @author: mumble-07

import board
import busio
import math
from math import pow, log
import time
from time import sleep,strftime
from datetime import datetime
import os
import glob
import time
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
time_interval = .2 #in secs
iteration = 5 #times
#================= TGS-2600 Definition =================
RL_2600 = 20000 #in ohm RL min
Ro_2600 = 41000 #in Ohm
Ro_factor_2600 = 1
#================= TGS-2602 Definition =================
RL_2602 = 4700 #in ohm RL min
Ro_2602 = 41000 #in Ohm
Ro_factor_2602 = 1
#================= TGS-2611 Definition =================
RL_2611 = 4700 #in ohm RL min
Ro_2611 = 41000 #in Ohm
Ro_factor_2611 = 9
#================= TGS-2620 Definition =================
RL_2620 = 4700 #in ohm RL min
Ro_2620 = 41000 #in Ohm
Ro_factor_2620 = 20


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
Rs_read_2600 = rs_read_sensor (TGS_2600, Vc, RL_2600, time_interval, iteration)
Rs_read_2602 = rs_read_sensor (TGS_2602, Vc, RL_2602, time_interval, iteration)
Rs_read_2611 = rs_read_sensor (TGS_2611, Vc, RL_2611, time_interval, iteration)
Rs_read_2620 = rs_read_sensor (TGS_2620, Vc, RL_2620, time_interval, iteration)
print ("2600: ", Rs_read_2600, "2602: ", Rs_read_2602, "2611: ", Rs_read_2611, "2620: ", Rs_read_2620)

