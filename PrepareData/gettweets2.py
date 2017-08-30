import tweepy
import datetime
import pickle


files=['For_profit_organizations','media','Non_profit_organizations','Personalities','ordinary']

allfeatures,alllabels=[],[]

for i in range(5):
    a=open('../Data/'+files[i]+'.csv')
    b=a.readlines()
    screennames=b[0].split('\r')
    screennames=map(lambda x:x.strip(),screennames)
    a.close()
    CONSUMER_KEY = "UfKQzmcJDqHRJQiC2Ipo4gKL8"
    CONSUMER_SECRET = "EBVJQxmZXGPxzEjUb3XVy7GokykKyjOGLRGN2vu57R8m9NTKf4"
    
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    
    api = tweepy.API(auth,wait_on_rate_limit=True)
    features,label=[],[]
    for sn in screennames:
        
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
            label.append(i)
        except BaseException:
            print sn
    
    f={"features":features,'label':label}
    print files[i]
    print len(features),len(label)
    
    allfeatures=allfeatures+features
    alllabels=alllabels+label
    
    pickle.dump(f,open(files[i]+".txt",'wb'))
    
allf={"features":allfeatures,'label':alllabels}
print len(allfeatures),len(alllabels)
pickle.dump(allf,open("allfeatures.txt",'wb'))

