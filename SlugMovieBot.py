import random
import commands
import xml.dom.minidom
from BeautifulSoup import BeautifulSoup
import re
from imdb import IMDb

class SlugMovieBot:
	def __init__(self):
		#@ TwitterIndex environment configuration, you don't need to read this part.
		self.twitter_data_set = ""
		self.twitter_file_path = "./twitter_corpus"
		self.twitter_file_name = "twitter.trectext"
		self.twitter_query_file = "query_params"
		self.twitter_index_path = "./index"
		self.max_twitter_number_retrieved = 100
		with open(self.twitter_file_path+"/"+self.twitter_file_name,'r') as f:
			self.twitter_data_set = f.read()
			f.close()
		self.twitter_soup = BeautifulSoup(''.join(self.twitter_data_set))
		#@ interface among functions
		self.twitter_index_keywords = "Avatar" #used by TwitterIndex, iMDBIndex should provide this parameter.
		self.imdb_index_keywords = "" #used by iMDBIndex, QReadAndAnalysis should provide this parameter.

	def QReadAndAnalysis(self):
		question = input("Q: ")
		"wrtie the result to imdb_index_keywords"
		pass

	#def iMDBIndex(self):
	#	"wrtie the result to twitter_index_keywords"
	#	pass
	
	# This method takes a string as the movie_name and a list of movie_keywords.
	# A movie_keyword is some information that you want to know about the movie.
	# It returns an array with answers to the data requested in movie_keywords.
	# Valid options in the list of movie_keywords are: director, runtime, actors, 
	# year released, film rating, imdb rating, writers, languages, plot, plot outline,
	# producers, production companies, and distributors. If an invalid movie_keyword 
	# is provided, then None is inserted into the returned array for that value.
	def imdbIndex(movie_name, movie_keywords):
		imdbAccess = IMDb()
		s_result = ia.search_movie(movie_name)
		if not s_result:
			return None
		movie = s_result[0]
		imdbAccess.update(movie)
		options = {'director': movie['director'][0], 'runtime': movie['runtime'][0], 'actors': getData(movie, 'cast'), 
				'year released': movie['year'], 'film rating': movie['mpaa'], 'imdb rating': movie['rating'], 
				'writers': getData(movie, 'writer'), 'languages': getData(movie, 'languages'), 'plot': getData(movie, 'plot'), 
				'plot outline': movie['plot outline'], 'producers': getData(movie, 'producer'), 
				'production companies': getData(movie, 'production companies'), 'distributors': getData(movie, 'distributors')}
		retrieved_information = []
		for keyword in movie_keywords:
			if keyword in options.keys():
				retrieved_information.append(options[keyword])
			else:
				retrieved_information.append(None)
		return retrieved_information
	
	# Returns imdb data as a readable string for person objects, company objects, etc.
	def getData(movie, option):
		total_data = ''
		for data in movie[option]:
			total_data += str(data) + ', '
		return total_data

	# retrieve a piece of twitter. 
	# twitter_index_keywords is the input
	def TwitterIndex(self):
		# step 0: initial information declaration.
		twitter_query_command = 'IndriRunQuery ' + self.twitter_query_file + \
								' -count='+str(self.max_twitter_number_retrieved)
		stanford_corenlp_query_command = 'java -cp "stanford/*" -mx5g \
										edu.stanford.nlp.sentiment.SentimentPipeline \
										-file stanford/sentiment.txt'
		query_parames = "<parameters>\n<index>" + self.twitter_index_path +\
				"</index>\n<query>\n<number>1</number>\n<text>" + self.twitter_index_keywords +\
				"\n</text>\n</query>\n<memory>1G</memory>\n<runID>runName</runID>\n \
				<trecFormat>true</trecFormat>\n</parameters>\n"
		with open(self.twitter_query_file, 'w') as f:
			f.write(query_parames)
			f.close()
		sentiment_file = "./stanford/sentiment.txt"
		twitter = "" # return to user.
		positive_twitter_list = []
		negative_twitter_list = []
		neutral_twitter_list = []
		# step 1: twitter query by tool indri 5.0; save twitters retrieved into sentiment.txt file.
		(status, query) = commands.getstatusoutput(twitter_query_command)
		if query == "":
			return "no information found!"
		query = query.split("\n")
		twitter_number_retieved = min(self.max_twitter_number_retrieved, len(query))
		with open(sentiment_file, 'w') as f:
			for i in range(0, twitter_number_retieved):
				docno = query[i].split(" ")[2]
				twitter =  self.twitter_soup.find('docno', text = re.compile(docno)).parent.findNextSibling('text').text
				f.write(twitter+'\n')
			f.close()
		# step 2: classify twitters into 3 groups: positive, negative, and neutral.
		# using stanford corenlp.
		(status, query) = commands.getstatusoutput(stanford_corenlp_query_command)
		sentiment_result = query.split("Adding annotator sentiment\n")[1].split('\n')
		for i in range(1, len(sentiment_result), 2):
			sentiment = sentiment_result[i].split(" ")[-1].lower()
			if sentiment=='positive':
				positive_twitter_list.append(sentiment_result[i-1])
			elif sentiment=='negative':
				negative_twitter_list.append(sentiment_result[i-1])
			else:
				neutral_twitter_list.append(sentiment_result[i-1])	
		# step 3: return a twitter according some kind of scoring rules.
		print "pos: ", positive_twitter_list
		print "neg: ", negative_twitter_list
		print "neu: ", neutral_twitter_list
		return twitter

	def chatbot(self):
		movieAnalysis = QReadAndAnalysis()
		movieInfo = iMDBIndex()
		twitterComments = TwitterIndex()
		print("A: " + twitterComments)

if __name__=="__main__":
	moviebot = SlugMovieBot()
	"""while True:
		moviebot.chatbot()"""
	moviebot.TwitterIndex()
