# Slug-MovieBot
We are a team of graduate students from UCSC. In this project, we are focussing on building a functional chat-bot that answers questions about movies. In addition, we aim at incorporating the ability to offer an opinion on the question asked based on public opinion from Tweets about the same. This is an extension on MovieBot (https://www.amazon.com/dp/B01MRKGF5W), so as to provide more of a human touch to the bot by adding an opinion to the responses to the questions asked by a user.

# Installation and running instructions
>1. INDRI-5.0 install commands:

./configure

make

make install

>2. Beautiful Soup 3.2 for python 2.7:

pip install beautifulsoup

>3. In the Slug-MovieBot directory run:

IndriBuildIndex query_parameter_file

This will generate an index folder which would be used as twitter data indexing.

>4. Setting up the twitter corpus: 

Change "filePath" in [./DataExtractionAndPreprocess/main.py](./DataExtractionAndPreprocess/main.py) to the path with your extracted tweets, stored in .json files. Run [./DataExtractionAndPreprocess/main.py](./DataExtractionAndPreprocess/main.py) to obtain tweets.xml. Convert this to a .trectext file and store in [./twitter_corpus](./twitter_corpus).

Note: .trectext files must be unix format.

>5. Stanford coreNLP:

Download Stanford coreNLP and change its folder name to stanford. Copy this folder in the Slug-MovieBot directory.

>6. LanguageTool Grammar-check: 

Install LanguageTool (https://www.languagetool.org/) and install the grammar-check package (https://pypi.python.org/pypi/grammar-check/1.3.1): pip install --user --upgrade grammar-check

>7. Run [SlugMovieBot.py](SlugMovieBot.py)
