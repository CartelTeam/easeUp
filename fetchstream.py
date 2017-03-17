from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import urllib
from .models import tweet,Profile
from django.contrib.auth.models import User
from django.conf import settings
#from django.contrib.auth.models import User
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream
a=[]

ckey = 'OWuUU4mRGdn8tar9hX7sK6Gez'
csecret = 'di3ZlQrPfLo6ZnlHcT5rf5fEhKWl0872LGuTCPn0ePe0uTDZOc'
atoken = 'a797431307319930880-LdUAqkmXPpY7eRbXGopnp5xPpiVM81H'
asecret= 'aiP8EJeroG9srijIkV4GDtI2OcqGIrjV24VXg1SNI4tHAT'


    


class myclass:
    def __init__(self,pro):
        
        #user=Profile.objects.filter(user=request.decode('ascci'))
        #pr=Profile()
        #for i in Profile.objects.all():
            #pr=i

        i=Profile.objects.filter(user_name=pro)
        self.usr=i[0].user_name
        self.atoken=i[0].oauth_token
        self.asecret=i[0].oauth_secret
        f=open('a.txt','a')
        f.write(self.atoken)
        f.write(i[0].user_name)
        f.write(self.asecret)
        f.write(str(type(self.atoken)))
        f.close()
        oauth = OAuth(self.atoken,self.asecret,settings.TWITTER_TOKEN,settings.TWITTER_SECRET)

        # Initiate the connection to Twitter Streaming API
        self.twitter_stream = TwitterStream(auth=oauth)
        self.val = [[]]
        self.b = []
        s = "1990"
        self.val[0].append(s)
    def get_tweet(self,string):

        self.iterator = self.twitter_stream.statuses.filter(track=string,languages='en')
        
        
        tweet.objects.filter(user_name=self.usr).delete()

        self.tweet_count = 100
        for self.tweet1 in self.iterator:
            self.tweet_count -= 1
            self.tweet_ = json.dumps(self.tweet1)
            try:
                self.t = json.loads(self.tweet_)
                self.st=self.t["text"]

                obj = tweet(tweets=self.st, user_name=self.usr)
                obj.save()
                try:
                    cordinate = self.t["coordinates"]
                    if cordinate is not None:

                        self.b.append(cordinate['coordinates'][0])
                        self.b.append(cordinate['coordinates'][1])
                        self.b.append(1)

                except:
                    pass

                if self.tweet_count <= 0:
                    self.val[0].append(self.b)
                    f = open('webapp/static/globe/population909500.json', 'w')
                    f.write(json.dumps(self.val))

                    f.close()
                    break
            except:
                pass


        #self.twitterStream.disconnect()

