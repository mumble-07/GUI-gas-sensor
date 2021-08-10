# Created by TheGullibleKid at 8/09/2021
# @author: mumble-07
import board
import busio
import math
import time
from time import sleep,strftime
from datetime import datetime
import os
import glob
import time
import RPi.GPIO as GPIO                    #Import GPIO library
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

            
GPIO.setmode(GPIO.BCM)                     #Set GPIO pin numbering

TRIG = 15                                  #Associate pin 15 to TRIG
ECHO = 14                                  #Associate pin 14 to Echo

GPIO.setup(TRIG,GPIO.OUT)                  #Set pin as GPIO out
GPIO.setup(ECHO,GPIO.IN)                   #Set pin as GPIO in

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

i2c =busio.I2C(board.SCL,board.SDA)

#===============GASSES CURVE==================
CO = float(1.11231525, -0.2216452, -0.26468)
Methane = float(1.038534, -0.0832604, -0.0945188)
Isobutane = float(0.740737467, -0.3019758439, -0.32013509)
Hydrogen = float(0.623847109, -0.3137123394, -0.3528411122)
Ethanol = float(0.613531029, -0.2820988119, -0.2738511645)

#=================GAS ====================

# GAS_Air
# GAS_Ethanol
# GAS_Methane
# GAS_Hydrogen
# GAS_co
# GAS_Isobutane

#====================GLOBALS ======================








#Source: http://sandboxelectronics.com/?p=165&fbclid=IwAR21hPZ3GicmXwsZtNprk5C9vpxRMSIU74ZGa0ehxBJ_Zb2yCtrNlJl3Hpg

