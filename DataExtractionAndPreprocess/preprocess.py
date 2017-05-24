import pandas
import re
import os

def preprocess(Data):
    fileread = pandas.read_csv(Data, error_bad_lines=False)
    cleanTweets = []
    tweetIds = []
    x = fileread[['text']].values.tolist()
    t = fileread[['tweet_id']].values.tolist()

    # print(x)

    # Regex to remove HTML tags
    HTMLreg = re.compile(r'<[^>]+>')
    # Regex to remove URLS
    URLreg = re.compile(r'http\S+|www\S+')
    # Regex to remove @ from Twitter handles
    HANDLEreg = re.compile(r'@')
    # Regex to remove trailing hashtags
    TRAILreg = re.compile(r'([ ]*#[\w%@!&]*[ ]*)+$')
    # Regex to remove \n from tweets
    NEWLINEreg = re.compile(r'\\n')
    # Regex to remove unicodes of emojis from tweets
    EMOJIreg = re.compile(r'\\u[0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z][0-9a-zA-Z]')
    # Regex to remove unicodes of emojis from tweets
    RETWEETreg = re.compile(r'^RT')

    for i in range(0, len(x)):
        [tweet] = x[i]
        [tweetID] = t[i]
        if re.search(RETWEETreg, tweet):
            # print(tweet)
            continue
        tweet = re.sub(HTMLreg, '', tweet)  # removing HTML tags
        tweet = re.sub(URLreg, '', tweet)  # removing URLs
        tweet = re.sub(HANDLEreg, '', tweet)  # removing @ from twitter handles
        tweet = re.sub(TRAILreg, '', tweet)  # removing trailing hashtags
        tweet = re.sub(NEWLINEreg, '', tweet)  # removing newline characters
        tweet = re.sub(EMOJIreg, '', tweet)  # removing emoji unicodes
        tweet = tweet.strip(' ').lstrip(' ')  # removing extra spaces left behind
        cleanTweets.append(tweet)
        tweetIds.append(tweetID)
    # print(cleanTweets)
    return cleanTweets, tweetIds

#test local - only run the preprocess to see what it does
# cleanTweets, tweetIds = preprocess("trump-50k.csv")