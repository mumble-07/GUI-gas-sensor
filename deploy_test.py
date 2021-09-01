# Created by TheGullibleKid at 8/27/2021
# @author: mumble-07

from math import gamma
from pandas import read_csv
from sklearn.model_selection import  train_test_split #we can ale to split the data for training and validation
from sklearn.svm import SVC #pip install scikit-learn

fileName = "ppm.csv"

names =['CO', 'Toluene', 'Ammonia','Methane', 'Ethanol', 'Isobutane'] #==> specifiy columns here 

#====================================================================================
# reading the data set, need natin to separate yung datas into different variables
#final column will be a different variable since dito yung parang result or status. 
# It will be a different variable dependent on the independent variables
#====================================================================================
dataset = read_csv(fileName, names = names) 

#============================SEGREGATION OF DATASET PART======================#

array = dataset.values 

x = array [:,0:5] # ==> 0:N **means going to take the top n data for X. ito yung results
y = array [:,6] #For y data 
#========================X is going to be the input and y is going to be the output============

#==========================SEGREGATION OF DATA TO TRAIN TEST===================================
#===========Four variables===========

X_train, X_validation, Y_train, Y_valdiation = train_test_split(x, y, test_size= 0.50, random_state=1)
#===>>> test size is ratio e.g. ).50 test size meaning 50% to  testing, 50% to training
#===>>> random_state = randomly it will choose the data to be part of percentage testing and percentage training



#========== MODEL IS TRAINING PART==========================
model = SVC(gamma = "auto") #SVS = Support vector Classifier, some of the tuning parameters

model.fit(X_train, Y_train) #----> it means we are going to train our model
print ("YEHEY! Training Complete")
import pickle #we are going to save our model in this pickle

fileName = 'mode_test.pkl ' #import model.pkl file here to be saved in this file local directory tung model data

pickle.dump(model, open(fileName, 'wb')) #-> write binary 
print ("Model  is saved!")
loaded_model = pickle.load (open(fileName, 'rb')) #===> read binary
result = loaded_model.score(X_validation, Y_valdiation) #====> score will be helpful in validating and valuating the model will help in knowing the performing score of our model
print (result) #model score/performance
value = [[1.075, 2.373, 5.164, 15.627, 60.72, 17.507]] #insert prediction static values
predictions = loaded.model.predict(value)
print (predictions[0])
