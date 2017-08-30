import tweepy
import datetime

label_number=1
a=open('../Data/screen_names.txt')
b=a.readlines()
screennames=b[0].split('\r')
screennames=map(lambda x:x.strip(),screennames)
a.close()
CONSUMER_KEY = "CONSUMER_KEY"
CONSUMER_SECRET = "ECONSUMER_SECRET"

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
        label.append(label_number)
    except BaseException:
        print sn
