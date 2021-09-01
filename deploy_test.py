from itertools import Predicate
from pandas import read_csv
from sklearn.model_selection import  train_test_split #we can ale to split the data for training and validation
from sklearn.svm import SVC #pip install scikit-learn

fileName = "log.csv"
names =[''] #==> specifiy columns here 

#====================================================================================
# reading the data set, need natin to separate yung datas into different variables
#final column will be a different variable since dito yung parang result or status. 
# It will be a different variable dependent on the independent variables
#====================================================================================
dataset = read_csv(fileName, name = names) 

#============================SEGREGATION OF DATASET PART======================#

array = dataset.values 

x = array [:,0:6] # ==> 0:N **means going to take the top n data for X. ito yung results
y = array [:,6] #For y data 
#========================X is going to be the input and y is going to be the output============

#==========================SEGREGATION OF DATA TO TRAIN TEST===================================
#===========Four variables===========

X_train, X_validation, Y_train, Y_valdiation = train_test_split(x, y, test_size= 0.50, random_state=1)
#===>>> test size is ratio e.g. ).50 test size meaning 50% to  testing, 50% to training
#===>>> random_state = randomly it will choose the data to be part of percentage testing and percentage training

model = SVC(gamme = "auto")

model.fit(X_train, Y_train)

import pickle

fileName = 'import model.pkl file here'

pickle.dump(model, open(fileName, 'wb'))

loaded_model = pickle.load (open(fileName, 'rb'))
result = loaded_model.score(X_validation, Y_valdiation)
print (result)

value = [[inser dummy values form csv or manual data]]
predictions = loaded.model.predict.value
print (predictions[0])
