import convertJSON_CSV as cjc
import preprocess as pp
import csv
import glob
import os
import pandas as pd

def saveCleanTweets(filename, cleanTweets, tweetIds):
    csvFile = filename.split("/csv")
    # csvFile = csvFile[1].split("\\")
    csvFilename = "./data/allTimeMovieTweets/movies-allTime/cleanedCSV/" + csvFile[1]
    dirname = os.path.dirname(csvFilename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    raw_data = {'tweet_id': tweetIds, 'text': cleanTweets}
    df = pd.DataFrame(raw_data, columns=['tweet_id', 'text'])
    df.to_csv(csvFilename)

#convert obtained JSON to CSV files. Can skip this step if done once before.
# filenames = glob.glob("./data/allTimeMovieTweets/movies-allTime/query-#101dalmatians-2017-05-10-09-43-14.json")
filenames = glob.glob("./data/allTimeMovieTweets/movies-allTime/*.json")
cjc.convert(filenames)

#to preprocess and clean the tweets
# dataSets = glob.glob("./data/allTimeMovieTweets/movies-allTime/csv/query-#101dalmatians-2017-05-10-09-43-14.csv")
dataSets = glob.glob("./data/allTimeMovieTweets/movies-allTime/csv/*.csv")
print(dataSets)
num = 0
for dataSet in dataSets:
    num += 1
    cleanTweets, tweetIds = pp.preprocess(dataSet)
    print ("Preprocessing " + str(num * 100 / len(dataSets)) + "% complete")
    # print (cleanTweets)
    saveCleanTweets(dataSet, cleanTweets, tweetIds)