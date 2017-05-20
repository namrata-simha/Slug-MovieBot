# Slug-MovieBot
We are a team of graduate students from UCSC. In this project, we are focussing on building a functional chat-bot that answers questions about movies. In addition, we aim at incorporating the ability to offer an opinion on the question asked based on public opinion from Tweets about the same. This is an extension on MovieBot (https://www.amazon.com/dp/B01MRKGF5W), so as to provide more of a human touch to the bot by adding an opinion to the responses to the questions asked by a user.

# contents added by Lixue
1. INDRI-5.0 install commands:

./configure

make

make install

2. Beautiful Soup 3.2 for python 2.7:

pip install beautifulsoup

3. In the Slug-MovieBot directory run:

IndriBuildIndex query_parameter_file

This will generate an index folder which would be used as twitter data indexing.

4. please convert twitter data into trectext format as sample in twitter_corpus.

warning: ***.trectext files must be unix format.

5. Download Stanford coreNLP and change its folder name to stanford. Copy this folder in the Slug-MovieBot directory.
