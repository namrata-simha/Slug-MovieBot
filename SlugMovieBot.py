import random
import commands
import xml.dom.minidom
from BeautifulSoup import BeautifulSoup
from imdb import IMDb
from IMDbPY import imdbData
from qlists import qlist
import re

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
        self.movie_name = ""
        self.movie_keywords = ""
        self.twitter_index_keywords = "" #used by TwitterIndex, iMDBIndex should provide this parameter.
        #@ twitter classification according to sentiment analysis.

    # retrieve a piece of twitter. 
    # twitter_index_keywords is the input
    def tweetSelection(self, very_pos_list, pos_list, very_neg_list, neg_list, neu_list):    
        #Deal with small lists
        if len(very_pos_list) <= 2:
            very_pos_list = very_pos_list + pos_list
        
        if len(very_neg_list) <= 2:
            very_neg_list = very_neg_list + neg_list              
        #Search for very positive or negative first
        target_list = []

        if len(very_pos_list) >= len(very_neg_list):
            target_list = very_pos_list
        else:
            target_list = very_neg_list           
        #Use neutral tweets as last resort       
        if len(target_list) <= 2 and len(neu_list)>0:
            target_list = neu_list        
        
        if len(target_list) <= 0:
            print 'not enough tweets to evaluate'
            return "nothing"     

        tweet_index = random.randint(0, len(target_list)-1)      
        return target_list[tweet_index]

    def TwitterIndex(self):
        # step 0: initial information declaration.
        twitter_query_command = 'IndriRunQuery ' + self.twitter_query_file + \
                                ' -count='+str(self.max_twitter_number_retrieved)
        stanford_corenlp_query_command = 'java -cp "stanford/*" -mx5g \
                                        edu.stanford.nlp.sentiment.SentimentPipeline \
                                        -file stanford/sentiment.txt'
        query_parames = "<parameters>\n<index>" + self.twitter_index_path +\
                "</index>\n<query>\n<number>1</number>\n<text>#combine( " + self.twitter_index_keywords +\
                " )\n</text>\n</query>\n<memory>1G</memory>\n<runID>runName</runID>\n \
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
        very_pos_list = [] 
        pos_list = []
        very_neg_list = []
        neg_list = [] 
        neu_list = []
        (status, query) = commands.getstatusoutput(stanford_corenlp_query_command)
        sentiment_result = query.split("Adding annotator sentiment\n")[1].lower().split('\n')
        for i in range(1, len(sentiment_result), 2):
            sentiment = sentiment_result[i]
            if sentiment=='  very positive':
                very_pos_list.append(sentiment_result[i-1])
            elif sentiment=='  very negative':
                very_neg_list.append(sentiment_result[i-1])
            elif sentiment=='  positive':
                pos_list.append(sentiment_result[i-1])
            elif sentiment=='  negative':
                neg_list.append(sentiment_result[i-1])
            else:
                neu_list.append(sentiment_result[i-1])    
        # step 3: return a twitter according some kind of scoring rules.
        return self.tweetSelection(very_pos_list, pos_list, very_neg_list, neg_list, neu_list)

    # used to detect movie name in Q.    
    def movie_name_detection(self, question, idx):
        """
        movie name: words between the first and last unmatched word
        """
        movie_name = ""
        # step 0: remove '.' and '?' in question
        qcopy = question
        qlen = len(qcopy) - 1
        if qcopy[qlen] == '.' or qcopy[qlen] == '?':
            qcopy = qcopy[0:qlen]
        qcopy = qcopy.split(" ")
        # step 1: construct dictionary.
        qlist_dict = set([])
        for word in qlist[idx]:
            qlist_dict.add(word)
        # step 2: check same.
        start_idx = -1
        end_idx = -1
        for i in range(0, len(qcopy)):
            if qcopy[i] not in qlist_dict:
                start_idx = i
                end_idx = i
                break
        for i in range(start_idx+1, len(qcopy)):
            if qcopy[i] not in qlist_dict:
                end_idx = i

        if start_idx == -1:
            return ""

        for i in range(start_idx, end_idx+1):
            movie_name += (qcopy[i] + ' ')
        movie_name = movie_name[0:len(movie_name)-1]
        # return movie name.    
        return movie_name

    def qsim(self, question_from_user):
        # step 1: construct input question dictionary.
        qlen = len(question_from_user) - 1
        if question_from_user[qlen]=='.' or question_from_user[qlen]=='?':
            question_from_user = question_from_user[0:qlen]
        question = question_from_user.lower().split(" ")
        qdict = set([])
        for word in question:
            qdict.add(word)
        # step 2: select a question from qlist with highest probability.
        prob = 0
        idx = 0
        for i in range(0, len(qlist)):
            wordcount = 0
            for word in qlist[i]:
                if word in qdict:
                    wordcount += 1
            local_prob = wordcount/float(len(qlist[i]))
            if local_prob > prob:
                prob = local_prob
                idx = i
        # step 3: return question idx.
        return idx+1

    def ConversationStrategy(self):
        # step 0: get user input
        question_from_user = raw_input("Q: ").lower()
        # step 1: find similar question from corpus
        idx = self.qsim(question_from_user)
        # step 2: retrieve movie name from user input
        self.movie_name = self.movie_name_detection(question_from_user, idx-1)
        # step 3: get imdb information.
        imdbOutput = imdbData(self.movie_name, idx)
        if imdbOutput is None:
            self.twitter_index_keywords = ""
		#"***********" + self.twitter_index_keywords +"\n\n\n"
        self.twitter_index_keywords = self.movie_name + " " + self.twitter_index_keywords
        # step 4: get twitter.
        twitter = self.TwitterIndex()
        # step 5: return 
        print "A: " + imdbOutput + "\n" + twitter

if __name__=="__main__":
    moviebot = SlugMovieBot()
    while True:
        moviebot.ConversationStrategy()
