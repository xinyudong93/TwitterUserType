
# two-phase classifier
# This classifier treat with 6 classes including Others
# Non-profit organization and for-profit organization are treated as one classes in first phase

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

import numpy as np
import copy
import pickle
import datetime


class TwoPhaseTwitterClassifier:
    
    def loadClassifierFromFile(self,class1,class2):
        self.clf1=pickle.load(open(class1))
        self.clf2=pickle.load(open(class2))
        pass
    
    def trainset(self,data):
        self.trainset=data
        pass
    
    def savemodel(self):
        file1=datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+"_two_phase_phase1.pkl"
        file2=datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+"_two_phase_phase2.pkl"
        with open(file1, 'wb') as f:
            pickle.dump(self.clf1, f)
        with open(file2, 'wb') as f:
            pickle.dump(self.clf2, f)
        pass
    
    def train(self,class1,class2):
        
        xy=self.trainset
        clf,clf2=DecisionTreeClassifier(),DecisionTreeClassifier()

    
        if class1=='svm':
            clf=SVC(kernel="linear",probability=True,max_iter=500)
        elif class1=='log':
            clf=LogisticRegression(penalty='l2', C=1,max_iter=500,solver='newton-cg')
        elif class1=='decisiontree':
            clf=DecisionTreeClassifier()
        elif class1=='knn':
            clf=KNeighborsClassifier()
    
        if class2=='svm':
            clf2=SVC(kernel="linear",probability=True,max_iter=500)
        elif class2=='log':
            clf2=LogisticRegression(penalty='l2', C=1,max_iter=500,solver='newton-cg')
        elif class2=='decisiontree':
            clf2=DecisionTreeClassifier()
        elif class2=='knn':
            clf2=KNeighborsClassifier()
    
        xy2=copy.deepcopy(xy)
        for i in range(len(xy)):
            if xy[i][11]==2:
                xy2[i][11]=0
    
        numberoftrain=len(xy)
        trainx,trainy,testx,testy=xy[:numberoftrain,:11],xy[:numberoftrain,11],xy[numberoftrain:,:11],xy[numberoftrain:,11]
        trainx2,trainy2,testx2,testy2=xy2[:numberoftrain,:11],xy2[:numberoftrain,11],xy2[numberoftrain:,:11],xy2[numberoftrain:,11]
    
        if class1=='svm':
            sc=StandardScaler()
            sc.fit(trainx2)
            trainx2=sc.fit_transform(trainx2)
            testx2=sc.fit_transform(testx2)
    
        clf.fit(trainx2,trainy2)
    
        rtrainx,rtrainy=[],[]
        if class2=='svm':
            sc=StandardScaler()
            sc.fit(trainx2)
            trainx2=sc.fit_transform(trainx2)
            testx2=sc.fit_transform(testx2)
    
            for i in range(len(trainx2)):
                if trainy[i]==0 or trainy[i]==2:
                    rtrainx.append(trainx2[i])
                    rtrainy.append(trainy[i])
        else:
            for i in range(len(trainx2)):
                if trainy[i]==0 or trainy[i]==2:
                    rtrainx.append(trainx2[i])
                    rtrainy.append(trainy[i])
            
        rtrainx=np.asarray(rtrainx)
        rtrainy=np.asarray(rtrainy)
    
        clf2.fit(rtrainx,rtrainy)

        self.clf1=clf
        self.clf2=clf2
        
        pass

    def test(self,xy):
        
        if self.clf1 is None:
            print "Have not trained any classifier"
            return
        
        xy2=copy.deepcopy(xy)
        for i in range(len(xy)):
            if xy[i][11]==2:
                xy2[i][11]=0
                
        testx,testy=xy[:,:11],xy[:,11]
        testx2,testy2=xy2[:,:11],xy2[:,11]
    
        predpro=self.clf1.predict_proba(testx)
        predy1=self.clf1.predict(testx)
        
        testx2phase=[]
    
        for i in range(len(predy1)):
            if predy1[i]==0:
                testx2phase.append(testx2[i])
                
        testx2phase=np.asarray(testx2phase)
    
        predy2=self.clf2.predict(testx2phase)
        predpro2=self.clf2.predict_proba(testx2phase)
    
        j=0
    
        predytotal=copy.deepcopy(predy1)
        notest=len(predy1)
        preprototal=np.zeros((notest,6))
        
        for i in range(len(predy1)):
            preprototal[i][1]=predpro[i][1]
            preprototal[i][3]=predpro[i][2]
            preprototal[i][4]=predpro[i][3]
            preprototal[i][5]=predpro[i][4]
            if predy1[i]==0:
                preprototal[i][int(predy2[j])]=predpro[i][0]
                predytotal[i]=predy2[j]
                j=j+1
    

    
        print "Recall:"
        print recall_score(testy,predytotal,average=None)
        
        print "Precision:"
        print precision_score(testy,predytotal,average=None)
        
        print "F1:"
        print f1_score(testy,predytotal,average=None)
        
        print "AUC:"
        for i in range(6):
            scorei=preprototal[:,i]
            fpr, tpr, thresholds =roc_curve(testy,scorei,pos_label=i)
            print auc(fpr,tpr)
        cm=confusion_matrix(testy,predytotal)
    
        print "confusion matrix:"
        print cm
    
        aa=0.0
        for i in range(5):
            aa+=cm[i][i]
        print "accuracy:",aa/notest
        pass
        
        
        
        
        
        
        