import tweepy           # To consume Twitter's API
import pandas as pd     # To handle data
import numpy as np      # For number computing



from textblob import TextBlob
import re



consumer_key = "rAezDfgG3lYjfbww4ez2NXbmi"
consumer_secret = "6kV4MSWE92V3Bt9wiiYPyjHGLZCnRjVTWhusyEz60aYg4f2bYn"
access_token = "1070694715476074496-3IDA1B5pGw5i2YEr0Fr2SM15jTuRMw"
access_token_secret = "yIAzga2LYtOYFm0ep7wtaxX2FoqUGcIAgU4juNDYb52Jr"

auth = tweepy.OAuthHandler("rAezDfgG3lYjfbww4ez2NXbmi", "6kV4MSWE92V3Bt9wiiYPyjHGLZCnRjVTWhusyEz60aYg4f2bYn")
auth.set_access_token("1070694715476074496-3IDA1B5pGw5i2YEr0Fr2SM15jTuRMw",
                      "yIAzga2LYtOYFm0ep7wtaxX2FoqUGcIAgU4juNDYb52Jr")

api = tweepy.API(auth)


# API's setup:
def twitter_setup():
    """
    Utility function to setup the Twitter's API
    with our access keys provided.
    """
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler("rAezDfgG3lYjfbww4ez2NXbmi", "6kV4MSWE92V3Bt9wiiYPyjHGLZCnRjVTWhusyEz60aYg4f2bYn")
    auth.set_access_token("1070694715476074496-3IDA1B5pGw5i2YEr0Fr2SM15jTuRMw", "yIAzga2LYtOYFm0ep7wtaxX2FoqUGcIAgU4juNDYb52Jr")

    # Return API with authentication:
    api = tweepy.API(auth)
    return api




screen_name = input("Enter Twitter Handle: ")
user = api.get_user(screen_name)

print("\nTWITTER\n")
print("Name: "+ user.name)
print("Twitter Handle: "+ screen_name)
print("\n")

# We create an extractor object:
extractor = twitter_setup()


# We create a tweet list as follows:
tweets = extractor.user_timeline(screen_name=screen_name, count=200)


# We print the most recent 5 tweets:
print(screen_name + "'s 5 most recent tweets:\n")
for tweet in tweets[:5]:
        print(tweet.text)
        print()


print("\n" + user.name + " most recent {:,d}".format(len(tweets)) + " tweets analyzed below.")



# We create a pandas dataframe as follows:
data = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

# We display the first 10 elements of the dataframe:
#display(data.head(10))


# Specific tweet
#
# print("Favorite Count: " + str(tweets[0].favorite_count))
# print("Retweet Count: " + str(tweets[0].retweet_count))


def clean_tweet(tweet):
    '''
    Utility function to clean the text in a tweet by removing
    links and special characters using regex.
    '''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

def analize_sentiment(tweet):
    '''
    Utility function to classify the polarity of a tweet
    using textblob.
    '''
    analysis = TextBlob(clean_tweet(tweet))
    if analysis.sentiment.polarity > 0:
        return 1
    elif analysis.sentiment.polarity == 0:
        return 0
    else:
        return -1

data['len']  = np.array([len(tweet.text) for tweet in tweets])
data['ID']   = np.array([tweet.id for tweet in tweets])
data['Date'] = np.array([tweet.created_at for tweet in tweets])
data['Source'] = np.array([tweet.source for tweet in tweets])
data['Likes']  = np.array([tweet.favorite_count for tweet in tweets])
data['RTs']    = np.array([tweet.retweet_count for tweet in tweets])
data['SA'] = np.array([ analize_sentiment(tweet) for tweet in data['Tweets'] ])

# We display the updated dataframe with the new column:
#display(data.head(10))

# We construct lists with classified tweets:

pos_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] > 0]
neu_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] == 0]
neg_tweets = [ tweet for index, tweet in enumerate(data['Tweets']) if data['SA'][index] < 0]


# We extract the tweet with more FAVs and more RTs:

fav_max = np.max(data['Likes'])
rt_max  = np.max(data['RTs'])

fav = data[data.Likes == fav_max].index[0]
rt  = data[data.RTs == rt_max].index[0]

# Max FAVs:
print("\n" + "Most liked tweet: {}".format(data['Tweets'][fav]))
print("Number of likes: {:,d}".format(fav_max))
print("{} characters.\n".format(data['len'][fav]))




# Max RTs:
print("Most retweeted tweet: {}".format(data['Tweets'][rt]))
print("Number of retweets: {:,d}".format(rt_max))
print("{} characters.\n".format(data['len'][rt]))


tlen = pd.Series(data=data['len'].values, index=data['Date'])
tfav = pd.Series(data=data['Likes'].values, index=data['Date'])
tret = pd.Series(data=data['RTs'].values, index=data['Date'])

tfav.plot(figsize=(16,4), label="Likes", legend=True)
tret.plot(figsize=(16,4), label="Retweets", legend=True);






# We print percentages:

print("Percentage of positive tweets: {}%".format(len(pos_tweets)*100/len(data['Tweets'])))
print("Percentage of neutral tweets: {}%".format(len(neu_tweets)*100/len(data['Tweets'])))
print("Percentage de negative tweets: {}%".format(len(neg_tweets)*100/len(data['Tweets'])))
print("\n")
r=[]
f=[]



for tweet in tweets:
    r.append(tweet.retweet_count)
    f.append(tweet.favorite_count)
print("Total Retweets " + "{:,}".format(sum(r)))
print("Total Favorites " + "{:,}".format(sum(f)))
print("\n")


y=[]
x=[]
a=[]
b=[]

print("Number of tweets: " + "{:,d}".format(int(user.statuses_count)) + "\n")


users = tweepy.Cursor(api.followers, screen_name, count=10).items()
for i in range(0, 40):
    user = next(users)
    y.append(user.followers_count)
    x.append(user.screen_name)

'''
third = tweepy.Cursor(api.followers, x[1], count=10).items()
for i in x:
    user = next(third)
    a.append(user.followers_count)
    b.append(user.screen_name)

'''



user = api.get_user(screen_name)

print(user.name + " / " + screen_name + "'s Three Degrees of Influence")

print("")


print("1st degree of influence: " + "{:,d}".format(int(user.followers_count)))
print("2nd degree of influence: " + "{:,d}".format(int(sum(y))))
print("3rd degree of influence: " + "{:,d}".format(int(sum(a))))

print("")

print("1st degree of influence = The number of followers " + screen_name + " has.")
print("2nd degree of influence = The number of follower's followers of " + screen_name + ".")
print("3rd degree of influence = The number of follower's follower's followers of "+ screen_name + ".")
