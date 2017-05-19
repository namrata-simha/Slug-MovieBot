import pandas
import re
import os

def preprocess(Data):
    fileread = pandas.read_csv(Data, error_bad_lines=False)
    cleanTweets = []
    x = fileread[['text']].values.tolist()
    tweetIds = fileread['tweet_id'].values.tolist()

    # Regex to remove HTML tags
    HTMLreg = re.compile(r'<[^>]+>')
    # Regex to remove URLS
    URLreg = re.compile(r'http\S+|www\S+')
    # Regex to remove @ from Twitter handles
    HANDLEreg = re.compile(r'@')
    # Regex to remove trailing hashtags
    TRAILreg = re.compile(r'([ ]*#[\w%@!&]*[ ]*)+$')

    for i in range(0, len(x)):
        [tweet] = x[i]
        tweet = re.sub(HTMLreg, '', tweet)  # removing HTML tags
        tweet = re.sub(URLreg, '', tweet)  # removing URLs
        tweet = re.sub(HANDLEreg, '', tweet)  # removing @ from twitter handles
        tweet = re.sub(TRAILreg, '', tweet)  # removing trailing hashtags
        tweet = tweet.strip(' ').lstrip(' ')  # removing extra spaces left behind
        cleanTweets.append(tweet)
    return cleanTweets, tweetIds

#test local - only run the preprocess to see what it does
# cleanTweets, tweetIds = preprocess("trump-50k.csv")