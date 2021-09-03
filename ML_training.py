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


dataset = pd.read_csv("ppm.csv") 

array = dataset.values 
Xar = array [0:,1:7]
Xar1 = array [0:,1:2]
Xar2 = array [0:,2:3]
Xar3 = array [0:,3:4]
Xar4 = array [0:,4:5]
Xar5 = array [0:,5:6]
Xar6 = array [0:,6:7]

print(Xar)

#========== MODEL IS TRAINING PART==========================

X = Xar

model = IsolationForest(n_estimators=500,  max_samples=300, contamination=0.01, random_state=42)
model.fit(X)  # fit 10 trees  
#number = model.predict(X)  # fit the added trees

print ("YEHEY! Training Complete")


import pickle 
fileName = 'mode_test3.pkl ' 
pickle.dump(model, open(fileName, 'wb'))
print ("Model  is saved!")
loaded_model = pickle.load (open(fileName, 'rb')) 
number1 = loaded_model.predict(X)

y = array [0:,7:8]
print(y)
plt.scatter(number1,Xar1)
plt.axis('tight')
plt.show()



