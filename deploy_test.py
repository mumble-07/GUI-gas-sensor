from itertools import Predicate
from pandas import read_csv
from sklearn.model_selection import  train_test_split #we can ale to split the data for training and validation
from sklearn.svm import SVC

fileName = "log.csv"

names =['']

dataset = read_csv(fileName, name = names)

array = dataset.values

x = array [:,0:6]
y = array [:,6]

X_train, X_validation, Y_train, Y_valdiation = train_test_split(x, y, test_size=)

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
