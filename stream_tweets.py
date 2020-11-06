from tweepy.streaming  import StreamListener  
from tweepy import OAuthHandler
from tweepy import Stream

import credential

class listener(StreamListener):
    def on_data(self, data):
        print(data)
        return True
    def on_error(self, status):
        print(status)
    
if __name__ == "__main__":
    listen = listener()
    auth = OAuthHandler(credential.CONSUMER_KEY, credential.CONSUMER_SECRET)
    auth.set_access_token(credential.ACCESS_TOKEN, credential.ACCESS_TOKEN_SECRET)
    
    stream = Stream(auth, listen)
    stream.filter(track = [""])   #about