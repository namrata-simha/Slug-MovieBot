import convertJSON_CSV as cjc
import convertCSV_XML as ccx
import preprocess as pp
import csv
import glob
import os
import pandas as pd

# filePath = "./data/allTimeMovieTweets/movies-allTime/"
filePath = "./data/tweets/"

def saveCleanTweets(filename, cleanTweets, tweetIds):
    csvFile = filename.split("/csv")
    # csvFile = csvFile[1].split("\\")
    csvFilename = filePath + "cleanedCSV/" + csvFile[1]
    dirname = os.path.dirname(csvFilename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    raw_data = {'tweet_id': tweetIds, 'text': cleanTweets}
    df = pd.DataFrame(raw_data, columns=['tweet_id', 'text'])
    df.to_csv(csvFilename)

#convert obtained JSON to CSV files.
# filenames = glob.glob(filePath + "query-#101dalmatians-2017-05-10-09-43-14.json")
filenames = glob.glob(filePath + "*.json")
cjc.convert(filenames, filePath)

#to preprocess and clean the tweets
# dataSets = glob.glob(filePath + "csv/query-#101dalmatians-2017-05-10-09-43-14.csv")
dataSets = glob.glob(filePath + "csv/*.csv")
print(dataSets)
num = 0
for dataSet in dataSets:
    num += 1
    cleanTweets, tweetIds = pp.preprocess(dataSet)
    print ("Preprocessing " + str(num * 100 / len(dataSets)) + "% complete")
    # print (cleanTweets)
    saveCleanTweets(dataSet, cleanTweets, tweetIds)

#convert obtained cleaned CSV to XML files.
# listOfMovies = []
# filenames = glob.glob(filePath + "cleanedCSV/query-#101dalmatians-2017-05-10-09-43-14.csv")
filenames = glob.glob(filePath + "cleanedCSV/*.csv")
ccx.convert(filenames)