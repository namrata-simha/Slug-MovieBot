import glob
import csv
import os
import pandas as pd

def convert(filenames):
    for filename in filenames:
        tweetTexts = []
        # tweetTexts.append('text')
        tweetIds = []
        # tweetIds.append('tweet_id')
        i = -1
        with open(filename) as f:
            for line in f:
                #make a list of all tweet ids
                tweetId = str(line).split(', "id": ')
                tweetId = tweetId[1].split(",")
                tweetIds.append(str(tweetId[0]))
                print(str(tweetId[0]))

                #make a list of all tweet texts
                text = str(line).split(', "text": "')
                text = text[1].split('", "truncated":')
                tweetTexts.append(text[0])
                print(text[0])


        #create a csv for the movie and write into csv
        csvFile = filename.split('/movies-allTime/')
        csvFile = csvFile[1].split(".json")
        csvFilename = "./data/allTimeMovieTweets/movies-allTime/csv/" + csvFile[0] + '.csv'
        dirname = os.path.dirname(csvFilename)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        raw_data = {'tweet_id': tweetIds,
                    'text': tweetTexts}
        # print(raw_data)
        df = pd.DataFrame(raw_data, columns=['tweet_id', 'text'])
        df.to_csv(csvFilename)


        # with open(csvFilename, 'rb') as csvfile:
        #     spamreader = csv.reader(csvfile, delimiter='|', quotechar='|')
        #     for row in spamreader:
        #         print ', '.join(row)

#test local - only run the convert to see what it does
# filenames = glob.glob("./data/allTimeMovieTweets/movies-allTime/*.json")
# filenames = glob.glob("./data/allTimeMovieTweets/movies-allTime/query-#101dalmatians-2017-05-10-09-43-14.json")
# convert(filenames)