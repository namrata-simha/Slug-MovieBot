# Slug-MovieBot
We are a team of graduate students from UCSC. In this project, we are focussing on building a functional chat-bot that answers questions about movies. In addition, we aim at incorporating the ability to offer an opinion on the question asked based on public opinion from Tweets about the same. This is an extension on MovieBot (https://www.amazon.com/dp/B01MRKGF5W), so as to provide more of a human touch to the bot by adding an opinion to the responses to the questions asked by a user.

# Installation and running instructions

IMPORTANT: Note that our code runs in Python 2.7 since the IMDbPY Python package only compiles in Python 2.7. 

>1. INDRI-5.0 install and configuration:

find indri 5.0 from lemur folder. link: https://sourceforge.net/projects/lemur/files/?source=navbar

find download files and run the following commands: 

./configure

make

make install

>2. Beautiful Soup 3.2 for python 2.7:

pip install beautifulsoup

>3. In the Slug-MovieBot directory run:

rm -rf index (comment: if you want to update the twitter dataset, you should first remove index folder, then generate it again. If this is the first time without index folder, no need to run this.)

IndriBuildIndex query_parameter_file

This will generate an index folder which would be used as twitter data indexing.

>4. Setting up the twitter corpus: 

Change "filePath" in [./DataExtractionAndPreprocess/main.py](./DataExtractionAndPreprocess/main.py) to the path with your extracted tweets, stored in .json files. Run [./DataExtractionAndPreprocess/main.py](./DataExtractionAndPreprocess/main.py) to obtain tweets.xml. Convert this to a .trectext file and store in [./twitter_corpus](./twitter_corpus).

Note: .trectext files must be unix format (you can use sublime to save the trectext file to UTF-8 format).

>5. Install IMDbPY python package:

pip install imdbpy

This will install the imdb python package that allows the code to fetch the factual response to each question in real time.

>6. Stanford coreNLP:

Download Stanford coreNLP and change its folder name to stanford. Copy this folder to the Slug-MovieBot directory.

>7. LanguageTool Grammar-check: 

Install LanguageTool (https://www.languagetool.org/) and install the grammar-check package (https://pypi.python.org/pypi/grammar-check/1.3.1):

pip install --user --upgrade grammar-check

(if you are working on linux platform. you can install this according to https://github.com/myint/language-check)

>8. Run [SlugMovieBot.py](SlugMovieBot.py)

python SlugMovieBot.py
