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
ads = ADS.ADS1015(i2c)
chan = AnalogIn(ads,ADS.P0)


#===============GASSES CURVE==================
CO = float(1.11231525, -0.2216452, -0.26468)
Methane = float(1.038534, -0.0832604, -0.0945188)
Isobutane = float(0.740737467, -0.3019758439, -0.32013509)
Hydrogen = float(0.623847109, -0.3137123394, -0.3528411122)
Ethanol = float(0.613531029, -0.2820988119, -0.2738511645)
# RO = float (10) #Initial value of RO

#=================GAS ====================

# GAS_Air
# GAS_Ethanol
# GAS_Methane
# GAS_Hydrogen
# GAS_co
# GAS_Isobutane

# TGS-2600 Definition
Vc = 5 #volts from data sheet
RL = 700 #in ohm
Ro = 24000 #in Ohm

#Calculating volate

volts = (chan * 3.3) / float(1023)
print 'volts:', volts

#Calculating Rs of TGS 2600
Rs = ((Vc*RL)/volts)-RL
print 'RS: ', Rs

#Calculating RS/RO ratio
Rs_Ro = Rs / Ro
Rs_Ro = round(Rs_Ro,2)
print "Rs_Ro: ", Rs_Ro

#=======CATEGORY==========

if Rs_Ro >= 1:
  Rs_Ro_stage = "Fresh air"
elif Rs_Ro < 1 and Rs_Ro >= 0.9:
  Rs_Ro_stage = ""
elif Rs_Ro < 0.9 and Rs_Ro >= 0.7:
  Rs_Ro_stage = ""
elif Rs_Ro < 0.7 and Rs_Ro >= 0.5:
  Rs_Ro_stage = ""
elif Rs_Ro < 0.5:
  Rs_Ro_stage = ""