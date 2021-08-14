# Created by TheGullibleKid at 8/14/2021
# @author: mumble-07

import numpy as np
#======================TGS2600======================#

C2H5OH = np.array([0.2995093465,-3.148170562], dtype=float)
C4H10 = np.array([0.3555567714, -3.337882361], dtype=float)
H2 = np.array([0.3417050674, -2.887154835], dtype=float)

def MQResistanceCalculation():
  raw_adc = #value from adc, represent voltage
  rl_value = #load resistance on board, in OHMS

    return float ((1024*1000*rl_value)/raw_adc-rl_value)

  