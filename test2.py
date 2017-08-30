'''
Created on Aug 30, 2017

@author: dongxinyu
'''
import os
import numpy as np
import pickle
import datetime
import json

from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import auc
from sklearn.metrics import roc_curve
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler

from Classifier import TwoPhaseTwitterClassifier,TwoPhaseTwitterClassifier2,TwoPhaseTwitterClassifier3,TwoPhaseTwitterClassifier4
#os.chdir('Desktop/Twitter_User_types')

f=pickle.load(open('Features/allfeatures.txt'))
features=f['features']
label=f['label']
for i in range(len(features)):
    features[i].append(label[i])

xy=np.asarray(features)
print xy.shape
np.random.shuffle(xy)


f=pickle.load(open('Features/opioid_features.txt'))
features=f['feature']
label=f['label']
for i in range(len(features)):
    features[i].append(label[i])

xyf=np.asarray(features)
xyf=filter(lambda x:x[-1]<5,xyf)
xyf=np.asarray(xyf)

print "Classifier2:"

tptc2=TwoPhaseTwitterClassifier2.TwoPhaseTwitterClassifier2()
tptc2.trainset(xy)
tptc2.train("decisiontree","decisiontree")
tptc2.test(xyf)
tptc2.savemodel()








