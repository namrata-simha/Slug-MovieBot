import random
import commands
import xml.dom.minidom
#python 3 from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup
import re

class SlugMovieBot:
	def __init__(self):
		self.twitter_data_set = ""
		self.twitter_file_path = "./twitter_corpus"
		self.twitter_file_name = "twitter.trectext"
		self.twitter_query_file_path = "query_params"
		with open(self.twitter_file_path+"/"+self.twitter_file_name,'r') as f:
			self.twitter_data_set = f.read()
			f.close()
		#twitter_soup = BeautifulSoup(twitter_data_set, "html.parser")
		self.twitter_soup = BeautifulSoup(''.join(self.twitter_data_set))
	###################################################################
	# read the question from keyboard input, like:
	# who is the director of Avatar?
	# output of this function should be a list like:
	# ["Avatar", "James Cameron"]
	###################################################################
	def QReadAndAnalysis(self):
		question = input("Q: ")
		"""
		put your code here........
		"""
		pass
	###################################################################
	# retrieve some objective information about a movie from analysis of
	# function QReadAndAnalysis()
	# example: 
	# movie_title = "Avatar"
	# movie_figure = "director"
	# imdb_dataset_path = "../../imdb.txt"
	# return: "James Cameron" + movie_title
	###################################################################
	def iMDBIndex(self, movie_title, movie_figure, imdb_dataset_path):
		pass
	###################################################################
	# retrieve twitter comments. example: 
	# input:
	# movie_description = "Avatar James Cameron"
	# twitter_dataset_path = "../../twitter.trectext"
	# output
	# return: "a piece of twitter"
	###################################################################
	def TwitterIndex(self, movie_description, twitter_dataset_path):
		global twitter_soup
		# step 1: construct a query.
		query_parames = "<parameters>\n<index>" + twitter_dataset_path +\
				"</index>\n<query>\n<number>1</number>\n<text>" + movie_description +\
				"\n</text>\n</query>\n<memory>1G</memory>\n<runID>runName</runID>\n \
				<trecFormat>true</trecFormat>\n</parameters>\n"
		with open("query_parames", 'w') as f:
			f.write(query_parames)
			f.close()
		# step 2: query and withdraw doc number.
		(status, query) = commands.getstatusoutput('IndriRunQuery query_parames -count=10')
		if query == "":
			return "no information found!"
		query = query.split("\n")
		index = random.randint(0,len(query)-1)
		docNo = query[index].split(" ")[2]
		# step 3: use docNo to search dataset to retrieve response.
		# python 3.0 should write like this
		# twitter =  self.twitter_soup.find('docno', string = re.compile(docNo)).find_next_sibling().get_text()
		# python 2.7		
		twitter =  self.twitter_soup.find('docno', text = re.compile(docNo)).parent.findNextSibling('text').text
		print twitter
		# step 4: return a response.
		return twitter

	def chatbot(self):
		movieAnalysis = QReadAndAnalysis()
		movieInfo = iMDBIndex(movieAnalysis[0], movieAnalysis[1], imdb_dataset_path)
		twitterComments = TwitterIndex(movieInfo, self.twitter_file_path)
		print("A: " + twitterComments)

if __name__=="__main__":
	moviebot = SlugMovieBot()
	"""while True:
		moviebot.chatbot()"""
	moviebot.TwitterIndex("Avatar","index")












