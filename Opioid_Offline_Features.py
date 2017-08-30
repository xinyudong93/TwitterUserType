import json
import datetime
import pickle
import numpy as np

result='Data/opioid_result.csv'

rf=open(result,'r')

lines=rf.readlines()

lines=lines[0].split('\r')

map2={'For-profit organizations':0,'Journalists/Media/News':1,'Non-profit organizations':2,'Personalities':3,'Ordinary Individuals':4,'Other':5}

aa,features,labels,yyy=[],[],[],[]

for line in lines:
    filename=line.split(',')[0].split('/')[1]
    aa.append(filename)
    filename=line.split(',')[1]
    labels.append(filename)

for label in labels:
    yyy.append(map2[label])

for a in aa:
    filen="To_Tag/"+a+".txt"
    file1=open(filen)
    lines=file1.readlines()
    file1.close()

    indegree=json.loads(lines[0])['user']['followers_count']
    outdegree=json.loads(lines[0])['user']['friends_count']

    user_favourite_count=json.loads(lines[0])['user']['favourites_count']
    user_listed_count=json.loads(lines[0])['user']['listed_count']
    retweet_count=0
    favourite_count=0

    verified=0
    if json.loads(lines[0])['user']['verified']==True:
        verified=1

    urls=0.0
    mentions=0.0

    retweeted=0.0
    for line in range(0,len(lines)):
        retweet_count+=(json.loads(lines[line])['retweet_count'])
        favourite_count+=(json.loads(lines[line])['favorite_count'])

        if len(json.loads(lines[line])['entities']['urls'])>0:
            urls+=1

        if len(json.loads(lines[line])['entities']['user_mentions'])>0:
            mentions+=1                   

        if json.loads(lines[line])['retweeted']:
            retweeted+=1

    retweeted_frac=retweeted/len(lines)
    mentions_frac=mentions/len(lines)
    urls_frac=urls/len(lines)

    postin3month=0
    date0=json.loads(lines[0])['created_at']
    date=datetime.datetime.strptime(date0,'%a %b %d %H:%M:%S +0000 %Y')
    for line in range(1,len(lines)):
        date1=json.loads(lines[line])['created_at']
        date1=datetime.datetime.strptime(date1,'%a %b %d %H:%M:%S +0000 %Y')
        d3=date-date1
        if d3.days<=90:
            postin3month+=1
    feature=[indegree,outdegree,postin3month,user_favourite_count,retweeted_frac,mentions_frac,urls,favourite_count,user_listed_count,retweet_count,verified]
    features.append(feature)

for i in range(len(features)):
    features[i].append(yyy[i])
features=np.asarray(features)

f={'feature':features,'label':yyy}

pickle.dump(f,open('offline_opioid_features.txt','wb'))





