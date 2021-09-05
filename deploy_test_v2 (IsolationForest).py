# Created by TheGullibleKid at 8/27/2021
# @author: mumble-07

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from sklearn.model_selection import  train_test_split
from sklearn.ensemble import IsolationForest


fileName = "ppm.csv"

names =['CO', 'Toluene', 'Ammonia','Methane', 'Ethanol', 'Isobutane'] 

import pickle 
fileName = 'mode_test3.pkl ' 
loaded_model = pickle.load (open(fileName, 'rb')) 
value = [[1.109,3.393,10.191,21.414,200.995,100.598]] #insert prediction static values
predictions = loaded_model.predict(value)
print (predictions)







