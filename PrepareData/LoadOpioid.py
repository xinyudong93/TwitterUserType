import os
import numpy as np
import pickle
import datetime
import json
import tweepy
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


result='../Data/opioid_result.csv'

rf=open(result,'r')

lines=rf.readlines()

lines=lines[0].split('\r')

map2={'For-profit organizations':0,'Journalists/Media/News':1,'Non-profit organizations':2,'Personalities':3,'Ordinary Individuals':4,'Other':5}

screen_names,features,labels,yyy=[],[],[],[]


CONSUMER_KEY = "UfKQzmcJDqHRJQiC2Ipo4gKL8"
CONSUMER_SECRET = "EBVJQxmZXGPxzEjUb3XVy7GokykKyjOGLRGN2vu57R8m9NTKf4"
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
api = tweepy.API(auth,wait_on_rate_limit=True)


for line in lines:
    filename=line.split(',')[0].split('/')[1]
    screen_names.append(filename)
    filename=line.split(',')[1]
    labels.append(filename)

for label in labels:
    yyy.append(map2[label])

for i in range(len(screen_names)):
    sn=screen_names[i]
    try:
        userid=api.get_user(sn).id
        tweets = api.user_timeline(id = userid, count = 1000)
        indegree=tweets[0]._json['user']['followers_count']
        outdegree=tweets[0]._json['user']['friends_count']
        user_favourite_count=tweets[0]._json['user']['favourites_count']
        user_listed_count=tweets[0]._json['user']['listed_count']
        retweet_count=0
        favourite_count=0
        verified=0
        if tweets[0]._json['user']['verified']==True:
            verified=1
 
        urls=0.0
        mentions=0.0
        retweeted=0.0
            
        for tweet in tweets:
            retweet_count+=(tweet._json['retweet_count'])
            favourite_count+=(tweet._json['favorite_count'])
    
            if len(tweet._json['entities']['urls'])>0:
                urls+=1
                        
            if len(tweet._json['entities']['user_mentions'])>0:
                mentions+=1                   
    
            if tweet._json['retweeted']:
                retweeted+=1
                    
        retweeted_frac=retweeted/len(tweets)
        mentions_frac=mentions/len(tweets)
        urls_frac=urls/len(tweets)
    
        postin3month=0
        date0=tweets[0]._json['created_at']
        date=datetime.datetime.strptime(date0,'%a %b %d %H:%M:%S +0000 %Y')
        for line in range(1,len(tweets)):
            date1=tweets[line]._json['created_at']
            date1=datetime.datetime.strptime(date1,'%a %b %d %H:%M:%S +0000 %Y')
            d3=date-date1
            if d3.days<=90:
                postin3month+=1
                    
        feature=[indegree,outdegree,postin3month,user_favourite_count,retweeted_frac,mentions_frac,urls_frac,favourite_count,user_listed_count,retweet_count,verified]
        features.append(feature)
        yyy.append(map2[labels[i]])
    except BaseException:
        print sn

print len(features),len(yyy)
f={'feature':features,"label":yyy}
pickle.dump(f,open('opioid_features.txt','w'))


#for i in range(len(features)):
#    features[i].append(yyy[i])
#features=np.asarray(features)

#f=pickle.load(open('features2.txt'))

#ffeatures=f['feature']

#newfeatures=np.concatenate((ffeatures,features))

#newf={'feature':newfeatures}

#pickle.dump(newf,open('features4.txt','w'))







