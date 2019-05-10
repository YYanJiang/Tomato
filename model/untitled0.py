#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 02:30:09 2018

@author: yanyanjiang
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC

from sklearn.metrics import accuracy_score



#movies = pd.read_csv('movie.csv')

#mov.info()
#X_train, X_test, Y_train, Y_test = model_selection.train_test_split(mov, y, test_size=test_size, random_state=seed)


X_train = pd.read_csv('x_train.csv')
#X_train = X_train.drop("theater_year", axis=1)
#X_train = X_train.drop('is_wide', axis=1)
idxx = X_train.index[ X_train['in_theater'] == 1]
X_train = X_train.loc[idxx]
#X_train = X_train[ X_train['in_theater'] == 1]

X_test = pd.read_csv('x_test.csv') 
#X_test = X_test.drop("theater_year", axis=1)
#X_test = X_test.drop("is_wide", axis=1)
#X_test = X_test[ X_test['in_theater'] == 1]
idxy = X_test.index[ X_test['in_theater'] == 1]
X_test = X_test.loc[idxy]

Y_train = pd.read_csv('y_train.csv',header = None)
Y_train = Y_train.loc[idxx]
Y_test = pd.read_csv('y_test.csv',header = None)
Y_test = Y_test.loc[idxy]





#print(X_train.shape,X_test.shape,Y_train.shape,Y_test.shape)
#-
#model = LogisticRegression(penalty='l2',dual=False, tol=0.0001, C=1.0,fit_intercept=True,
#                           intercept_scaling=1,class_weight=None,random_state=100, solver='liblinear', 
#                           max_iter=100, multi_class='ovr', verbose=0, warm_start=False, n_jobs=10 )
#model = RandomForestClassifier(n_estimators=2500,criterion="entropy",max_features='log2',random_state=150,max_depth=600,min_samples_split=163) #0.7795938583457157 +



#model = KNeighborsClassifier(n_neighbors=180, weights='uniform', algorithm='auto', leaf_size=5, p=1, metric='minkowski',n_jobs = 8)
model = DecisionTreeClassifier(min_samples_split=200, min_samples_leaf=2)  # 0.7684497275879149 +
#model = MLPClassifier(alpha=0.8,random_state=200)  #0.7847944526993561  -
#model = AdaBoostClassifier(n_estimators=150, learning_rate=1) #0.7852897473997028 +
#model =  SVC(C=0.5, kernel='linear', tol=0.05)   #0.7810797424467558    -


model.fit(X_train,Y_train)
predicted=model.predict(X_test)
print(model.feature_importances_)
#print(model.coef_)
acc = accuracy_score(Y_test,predicted)
print("accuracy is ",acc)


from sklearn.metrics import f1_score

print(f1_score(Y_test, predicted, average='macro'))
print(f1_score(Y_test, predicted, average='micro'))
print(f1_score(Y_test, predicted, average='weighted')) 

'''
features = X_train.columns
#importances = model.feature_importances_
#importances = model.coef_
indices = np.argsort(importances)

plt.title('Feature Importances')
plt.barh(range(len(indices)), importances[indices], color='b', align='center')
plt.yticks(range(len(indices)), [features[i] for i in indices])
plt.xlabel('Relative Importance')
plt.show()



models = []


models.append(('LR', LogisticRegression()))
models.append(('LDA', LinearDiscriminantAnalysis()))
models.append(('KNN', KNeighborsClassifier()))
models.append(('CART', DecisionTreeClassifier()))
models.append(('BNB', BernoulliNB()))
models.append(('mlr',linear_model.LinearRegression()))
models.append(('RF', RandomForestClassifier(n_estimators=2500, n_jobs=15,criterion="entropy",max_features='log2',random_state=150,max_depth=600,min_samples_split=163)))
models.append(('GBM', AdaBoostClassifier()))
models.append(('MLP', MLPClassifier()))
models.append(('SVC', SVC()))

results = []
names = []

from math import sqrt
for name, model in models:
    
    model.fit(X_train,Y_train)
    predicted=model.predict(X_test)
    
    print(model.feature_importances_)
    
    mse= mean_squared_error(Y_test.values,predicted)
    print(name, 'mean square error:', mse)   
    rmse = sqrt(mse)
    print(name, 'root mean square error:', rmse)
    
    acc = accuracy_score(Y_test.values,predicted)
    print("accuracy is ",acc)
# # # evaluate each model in turn
'''
