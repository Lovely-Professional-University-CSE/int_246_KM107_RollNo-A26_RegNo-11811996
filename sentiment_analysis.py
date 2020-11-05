import re
import tweepy
from textblob import TextBlob
import tkinter as Tk


def connect(query, count=10):

    consumer_key = ''
    consumer_secret = '' 
    access_token = ''
    access_secret = ''

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)
    results = api.search(q=query,count=count)

    tweets = []
        
    for tweet in results:
        parsed_tweet = {}
        parsed_tweet['text'] = tweet.text
        parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.text)
        if tweet.retweet_count > 0:
            if parsed_tweet not in tweets:
                tweets.append(parsed_tweet)
        else:
            tweets.append(parsed_tweet)
    return tweets


def cleantweet(tweet):

    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def get_tweet_sentiment(tweet):
    analysis = TextBlob(cleantweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'
 
def main():
    q,c = str(specifictweet.get()),int(tweetcount.get())
    tweets = connect(q,c)
    tweet_file  = open("file.txt","a")
    tweet_file.seek(0)
    tweet_file.truncate(0)
    tweet_file.write("analysis from Query: %s\n\n" %((str(q)).capitalize()))
    
   

    finalresult = ""
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    finalresult = "positive percentage: {} %".format(100*len(ptweets)/len(tweets)) + "\n"
    print("positive percentage: {} %".format(100*len(ptweets)/len(tweets)))
    
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    finalresult  = finalresult + ("negative percentage: {} %".format(100*len(ntweets)/len(tweets))) + '\n'
    print("negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))

    finalresult = finalresult + ("neutral percentage: {} % ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets))) + '\n'
    print("neutral tweets percentage: {} % ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))

    nutweets = []
    for tweet in tweets:
        if tweet not in ptweets and tweet not in ntweets:
            nutweets.append(tweet)
            
    tweet_file.write("Tweets Retrived: %d\n"%len(tweets))
    tweet_file.write("Results: \n")
    tweet_file.write(finalresult)
    tweet_file.write("\n\n")
    tweet_file.write("Positive tweets:\n\n")
    i = 1
    for tweet in ptweets:
        tweet_file.write(str(i) + ") ")
        tweet_file.write(tweet['text'].encode('utf-8'))
        tweet_file.write("\n\n")
        i = i+1
    tweet_file.write("Negative tweets:\n\n")
    i = 1
    for tweet in ntweets:
        tweet_file.write(str(i) + ") ")
        tweet_file.write(tweet['text'].encode('utf-8'))
        tweet_file.write("\n\n")
        i = i+1
    i = 1
    tweet_file.write("Neutral tweets:\n\n")
    for tweet in nutweets:
        tweet_file.write(str(i) + ") ")
        tweet_file.write(tweet['text'].encode('utf-8'))
        tweet_file.write("\n\n")
        i = i+1

    resultanalyzed.set(finalresult)
   
def for_sentence():
    result = hashtweet.get()
    result = get_tweet_sentiment(result)
    result = str(result)
    result = result.capitalize()
    resultanalyzed.set(result)



root = Tk.Tk()
root.title("SENTIMENT ANALYSIS")
root['bg'] = 'green'

tweetcount = Tk.IntVar()
hashtweet = Tk.StringVar()
specifictweet = Tk.StringVar()
resultanalyzed = Tk.StringVar()
eachtweet = Tk.StringVar()

tweetcount.set(0)
hashtweet.set("write a sentence")
specifictweet.set("any keyword")
resultanalyzed.set("")

frame1 = Tk.LabelFrame(root, text = "OPTIONS", bg = "#5EC365")
frame1.grid(row=0,column=0,padx = 10,pady = 10,sticky = 'nswe')
frame2 = Tk.LabelFrame(root,text="BUTTONS", bg = "#5EC365")
frame2.grid(row=0,column=1,padx = 10,pady = 10,sticky = 'nswe')
frame3 = Tk.LabelFrame(root,text="Result", bg = "#5EC365")
frame3.grid(row=1,column=0,columnspan = 2,padx = 10,pady = 10,sticky = 'nswe')
frame4 = Tk.LabelFrame(root,text="Tweets")
frame4.grid(row=2,column=0,columnspan = 2,padx = 10,pady = 10,sticky = 'nswe')

Tk.Label(frame1,text="Tweet Query: ").grid(row=0,sticky = 'w',padx = 10,pady = 10)
Tk.Label(frame1,text="Number of Tweets: ").grid(row=1,sticky = 'w',padx = 10,pady = 10)
Tk.Label(frame1,text="Specific Sentence: ").grid(row=2,sticky = 'w',padx = 10,pady = 10)

samplex = Tk.Entry(frame1,textvariable = specifictweet).grid(row=0,column=1,sticky='e',padx=5,pady=5)
sampley = Tk.Entry(frame1,textvariable = tweetcount).grid(row=1,column=1,sticky='e',padx=5,pady=5)
deltatime = Tk.Entry(frame1,textvariable = hashtweet).grid(row=2,column=1,sticky='e',padx=5,pady=5)


btn1 = Tk.Button(frame2,width=25,text="Analysis on Tweets",command=main, bg ="#61D0D0")
btn1.grid(row=0,column=0,padx = 10,pady = 10,sticky = 'nswe')
btn2 = Tk.Button(frame2,width=25,text="Analysis on a Specific Sentence",command=for_sentence, bg ="#61D0D0")
btn2.grid(row=1,column=0,padx = 10,pady = 10,sticky = 'nswe')
btn3 = Tk.Button(frame2,width=25,text="Save Results\nTo File", bg ="#61D0D0")
btn3.grid(row=2,column=0,padx = 10,pady = 10,sticky = 'nswe')

resultLabel = Tk.Label(frame3,textvariable=resultanalyzed)
resultLabel.grid(row=0,column=0,columnspan=2,sticky = 'nswe',padx=10,pady=10)

root.mainloop()