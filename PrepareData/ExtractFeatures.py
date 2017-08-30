
#extract features directly from downloaded tweets data.

import os
import json
import datetime
classes=['For_profit_organisations','Media_Outlets','Non_profit_organizations','Personalities','User_Data']

#map2=['For_profit_organisations':0,'Media_Outlets':1,'Non_profit_organizations':2,'Personalities':3,'Ordinary Individuals':4,'Other':5]

features=[]
label=[]

for j in range(5):

    type2=os.listdir(classes[j])
    
    for i in range(len(type2)):
        typei=type2[i]
        filename=classes[j]+"/"+typei
        file1=open(filename)
        lines=file1.readlines()
        file1.close()

        try:

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

            feature=[indegree,outdegree,postin3month,user_favourite_count,retweeted_frac,mentions_frac,urls_frac,favourite_count,user_listed_count,retweet_count,verified]
            features.append(feature)
            label.append(j)
            
        except BaseException:
            print classes[j],typei
            continue
        

