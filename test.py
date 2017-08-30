'''
Created on Aug 29, 2017

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
numberoftrain=len(xy)*2/3
trainxy,testxy=xy[:numberoftrain,:],xy[numberoftrain:,:]

print "Classifier2:"

tptc2=TwoPhaseTwitterClassifier2.TwoPhaseTwitterClassifier2()
tptc2.trainset(trainxy)
tptc2.train("decisiontree","log")
tptc2.test(testxy)
tptc2.savemodel()
print "Classifier4:"

tptc4=TwoPhaseTwitterClassifier4.TwoPhaseTwitterClassifier4()
tptc4.trainset(trainxy)
tptc4.train("decisiontree","log")
tptc4.test(testxy)
tptc4.savemodel()

f=pickle.load(open('Features/opioid_features.txt'))
features=f['feature']
label=f['label']
for i in range(len(features)):
    features[i].append(label[i])

xyf=np.asarray(features)
print xyf.shape
np.random.shuffle(xyf)
numberoftrain=len(xyf)*2/3
trainxy,testxy=xyf[:numberoftrain,:],xyf[numberoftrain:,:]

print "Classifier1:"

tptc1=TwoPhaseTwitterClassifier.TwoPhaseTwitterClassifier()
tptc1.trainset(trainxy)
tptc1.train("decisiontree","decisiontree")
tptc1.test(testxy)
tptc1.savemodel()


print "Classifier3:"

tptc3=TwoPhaseTwitterClassifier3.TwoPhaseTwitterClassifier3()
tptc3.trainset(trainxy)
tptc3.train("decisiontree","decisiontree")
tptc3.test(testxy)
tptc3.savemodel()















