""" This file is to train model """
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, roc_curve, auc
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from xgboost import plot_importance
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier

import warnings
warnings.filterwarnings("ignore")

feature_names = ['runtime', 'rating_G', 'rating_NR', 'rating_PG', 'rating_PG13', 'rating_R', 'rating_NC17',
                 'genre_action', 'genre_animation', 'genre_foreign', 'genre_classics', 'genre_comedy',
                 'genre_documentary', 'genre_drama', 'genre_horror', 'genre_family', 'genre_mystery', 'genre_romance',
                 'genre_fantasy', 'director_score', 'writer_score', 'actor_score', 'studio_score',
                 'theater_spring', 'theater_summer', 'theater_fall', 'theater_winter', 'theater_year', 'is_wide']

""" split train set and test set """
data = pd.read_csv('/Users/minghuijin/Desktop/RottenMovies/movie.csv')

X = data.drop(['Y', 'name', 'critic_score', 'audience_score'],axis=1)
y = pd.DataFrame(data['Y'], columns=['Y'])

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)


def plot_feature_importance(clf, feature_names):
    """ plot feature importance """
    plt.figure(figsize = (10, 10))
    feature_importance = clf.feature_importances_
    # make importances relative to max importance
    feature_importance = 100.0 * (feature_importance / feature_importance.max())
    sorted_idx = np.argsort(feature_importance)
    pos = np.arange(sorted_idx.shape[0]) + .5
    plt.barh(pos, feature_importance[sorted_idx], align='center')
    # plt.yticks(pos, feature_names[sorted_idx])
    plt.yticks(pos, [feature_names[idx] for idx in sorted_idx])
    plt.xlabel('Relative Importance')
    plt.title('Variable Importance')
    plt.show()

def compute_score(pred, true):
    """ compute accuracy_score and f1_score """
    accuracy = accuracy_score(pred, true)
    print("accuarcy score: %.2f%%" % (accuracy*100.0))

    f1 = f1_score(pred, true)
    print("f1 score: %.2f%%" % (f1*100.0))


""" 1. randomforest"""
print("************ RandomForest ************")
clf = RandomForestClassifier(n_estimators=150, max_depth=13, random_state=0)
clf.fit(x_train, y_train)
print()
y_pred = clf.predict(x_test)

compute_score(y_pred, y_test)

plot_feature_importance(clf, feature_names)


""" 2. xgboost """
print("************ XgBoost ************")
params = {'booster': 'gbtree',
          'objective': 'multi:softmax',
          'num_class': 2,
          'gamma': 0.2,
          'max_depth': 15,
          'lambda': 2,
          'subsample': 0.8,
          'colsample_bytree': 0.5,
          'min_child_weight': 2,
          'silent': 1,
          'eta': 0.1,
          'seed': 1000}

d_train = xgb.DMatrix(x_train, y_train)
num_rounds = 100
model = xgb.train(params, d_train, num_rounds)

dtest = xgb.DMatrix(x_test)
y_pred = model.predict(dtest)

compute_score(y_pred, y_test)

fig,ax = plt.subplots(figsize=(15,15))
plot_importance(model, height=0.5, ax=ax, max_num_features=64)
plt.show()

""" 3. AdaboostClassifier """
print("************ AdaboostClassifier ************")
clf = AdaBoostClassifier(n_estimators=120, learning_rate=0.9) 
clf.fit(x_train, y_train)
y_pred = clf.predict(x_test)

compute_score(y_pred, y_test)

plot_feature_importance(clf, feature_names)

""" 4. DecisionTreeClassifier """
print("************ DecisionTreeClassifier ************")
clf = DecisionTreeClassifier(min_samples_split=200, min_samples_leaf=8)
clf.fit(x_train, y_train)
pred = clf.predict(x_test)

compute_score(y_pred, y_test)

plot_feature_importance(clf, feature_names)

""" 5. Logistic Regression """
print("************ Logistic Regression ************")
clf = LogisticRegression(random_state=42, solver='lbfgs', multi_class='multinomial').fit(x_train, y_train)

y_pred = clf.predict(x_test)
compute_score(y_pred, y_test)

scores = clf.predict_proba(x_test)[:, 1]
fpr, tpr, thresholds = roc_curve(y_test, scores)  

plt.plot(fpr,tpr,marker = 'o')
plt.show()

AUC = auc(fpr, tpr)
print("AUC: %.2f%%" % (AUC*100.0))

""" 6. SVC """
print("************ SVC ************")
clf =  SVC(C=0.5, kernel='linear', tol=0.05).fit(x_train, y_train)

y_pred = clf.predict(x_test) 

compute_score(y_pred, y_test)

""" 7. OneVSRestClassifier """
print("************ OneVSRestClassifier ************")
clf = OneVsRestClassifier(SVC(C=2, cache_size=200, class_weight=None, coef0=0.2,decision_function_shape=None, 
                              degree=3, gamma='auto', kernel='linear',max_iter=-1, probability=False, 
                              random_state=42, shrinking=True,tol=0.005, verbose=False))

clf.fit(x_train,y_train)
y_pred = clf.predict(x_test)

compute_score(y_pred, y_test)

""" 8. KNeighborsClassifier """
print("************ KNeighborsClassifier ************")
clf = KNeighborsClassifier(n_neighbors=180, weights='uniform', algorithm='auto', leaf_size=5, p=1, metric='minkowski',n_jobs = 8)
clf.fit(x_train, y_train)
pred = clf.predict(x_test)

compute_score(y_pred, y_test)