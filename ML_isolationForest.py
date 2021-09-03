from deploy_test import X_train
import pandas as pd
import numpy as np

dataset = pd.read_csv("ppm.csv")

dataset.head()

X = dataset.iloc[:, 0:5].values
y = dataset.iloc[:, 5].values

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test = 0.2, random_steate = 0)

from sklearn.preprocession import StandardScaler 

sc = StandardScaler()

X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)

from sklearn.ensemble  import RandomForestClassifier

classifier = RandomForestClassifier(n_estimators = 20, random_state = 0)
classifier.fit(X_train, y_train)
y_pred = classifier.predict(X_test) 

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
print (confusion_matrix(y_test, y_pred))
print (classification_report(y_test, y_pred))
print(accuracy_score(y_test, y_pred))