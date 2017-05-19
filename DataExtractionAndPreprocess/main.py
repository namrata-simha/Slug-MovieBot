import convertJSON_CSV as cjc
import preprocess as pp
import csv
import glob
import os
import pandas as pd

def saveCleanTweets(filename, cleanTweets, tweetIds):
    csvFile = filename.split("/csv")
    csvFile = csvFile[1].split("\\")
    csvFile = csvFile[1].split(".csv")
    print(csvFile[0])
    csvFilename = "./data/allTimeMovieTweets/movies-allTime/cleanedCSV/" + csvFile[0] + '.csv'
    dirname = os.path.dirname(csvFilename)
    print(csvFilename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    raw_data = {'tweet_id': tweetIds,
                'text': cleanTweets}
    print(raw_data)
    df = pd.DataFrame(raw_data, columns=['tweet_id', 'text'])
    df.to_csv(csvFilename)

#convert obtained JSON to CSV files. Can skip this step if done once before.
filenames = glob.glob("./data/allTimeMovieTweets/movies-allTime/query-#101dalmatians-2017-05-10-09-43-14.json")
# filenames = glob.glob("./data/allTimeMovieTweets/movies-allTime/*.json")
cjc.convert(filenames)

#to preprocess and clean the tweets
dataSets = glob.glob("./data/allTimeMovieTweets/movies-allTime/csv/*.csv")
print(dataSets)
for dataSet in dataSets:
    cleanTweets, tweetIds = pp.preprocess(dataSet)
    print (cleanTweets)
    saveCleanTweets(dataSet, cleanTweets, tweetIds)