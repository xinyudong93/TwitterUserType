
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

#os.chdir('Desktop/Twitter_User_types')

f=pickle.load(open('Features/opioid_features.txt'))
features=f['feature']
label=f['label']
for i in range(len(features)):
    features[i].append(label[i])

xy=np.asarray(features)
print xy.shape
np.random.shuffle(xy)
numberoftrain=len(xy)*2/3
trainx,trainy,testx,testy=xy[:numberoftrain,:11],xy[:numberoftrain,11],xy[numberoftrain:,:11],xy[numberoftrain:,11]

#st=StandardScaler()
#st.fit(trainx)
#trainx=st.fit_transform(trainx)
#testx=st.fit_transform(testx)

clf=DecisionTreeClassifier()
#clf=LogisticRegression(penalty='l2', C=1,max_iter=500,solver='newton-cg')
#clf=SVC(kernel="linear",probability=True,max_iter=500)
#clf=KNeighborsClassifier()

#train
clf.fit(trainx,trainy)

#accuracy
print clf.score(testx,testy)
predy=clf.predict(testx)
predpro=clf.predict_proba(testx)

#recall, precision, f1
print recall_score(testy,predy,average=None)
print precision_score(testy,predy,average=None)
print f1_score(testy,predy,average=None)

#auc
for i in range(5):
    scorei=predpro[:,i]
    fpr, tpr, thresholds =roc_curve(testy,scorei,pos_label=i)
    print auc(fpr,tpr)

#confusion matrix
confusion_matrix(testy,predy)
