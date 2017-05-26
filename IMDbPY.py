'''

@author: alifsarker
'''

from imdb import IMDb
import random
#from IMDbPY import imdbData

def findKeyword(keyword):
    ia = IMDb()
    print ia.get_keyword(keyword)

def getDirectors(movie):
    ia = IMDb()
    s_result = ia.search_movie(movie)
    #print 'movie results:'
    #for result in s_result:
    #    print result
    #    for key in result.keys():
    #        print(key + ': ' + str(result[key]))
    movie_data = s_result[0]
    ia.update(movie_data)
    #print('first result:')
    #for stuff in movie_data.keys():
        #print (stuff + ': ' + str(movie_data[stuff]))
        #print(stuff + ': ')
        #print(movie_data[stuff])
    print movie_data['director'][0]

def getRuntimes(movie):
    ia = IMDb()
    s_result = ia.search_movie(movie)
    movie_data = s_result[0]
    ia.update(movie_data)
    print movie_data['runtime'][0]

def getDirector(movie):
    return movie['director'][0]

def getRuntime(movie):
    return movie['runtime'][0]
    
def getActors(movie):
    actors = ''
    for actor in movie['cast']:
        actors += str(actor) + ', '
    return actors

def getYear(movie):
    return movie['year']

def getFilmRating(movie):
    return movie['mpaa']

def getRating(movie):
    return movie['rating']
    
def questionProcessing(ia):
    movie = raw_input('What movie are you interested in talking about? ')
    s_result = ia.search_movie(movie)
    if not s_result:
        print 'Unfortunately I do not know anything about that movie.'
        return
    movie_data = s_result[0]
    ia.update(movie_data)
    print 'I know a lot about ' + str(movie_data['title']) + '!'
    print 'What would you like to know about ' + str(movie_data['title']) + '?'
    print '1: director'
    print '2: runtime'
    print '3: actors'
    print '4: year released'
    print '5: film rating'
    print '6: imdb rating' 
    while True:
        user_input = raw_input()
        if user_input.isdigit():
            processQuery(user_input, movie_data)
        else:
            break

# This method takes a string as the movie_name and a list of movie_keywords.
# A movie_keyword is some information that you want to know about the movie.
# It returns an array with answers to the data requested in movie_keywords.
# Valid options in the list of movie_keywords are: director, runtime, actors, 
# year released, film rating, imdb rating, writers, languages, plot, plot outline,
# producers, production companies, and distributors. If an invalid movie_keyword 
# is provided, then None is inserted into the returned array for that value.
def imdbIndex(movie_name, movie_keywords):
    imdbAccess = IMDb()
    s_result = imdbAccess.search_movie(movie_name)
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
    imdbAccess.update(movie, 'trivia')
    print movie['trivia']
    return retrieved_information

# Takes a movie name and option number from 1-15 and outputs the requested data.
def imdbData(movie_name, idx):
    if ((idx < 1) or (idx > 15)):
        return None
    imdbAccess = IMDb()
    s_result = imdbAccess.search_movie(movie_name)
    if not s_result:
        return None
    movie = s_result[0]
    imdbAccess.update(movie)
    if (idx == 10):
        imdbAccess.update(movie, 'quotes')
    if (idx == 12):
        imdbAccess.update(movie, 'trivia')
    options = {1: getData(movie, 'genres'),
               2: getData(movie, 'cast'),
               3: getData(movie, 'director'),
               4: getData(movie, 'writer'),
               5: movie.get('mpaa'),
               6: movie.get('year'),
               7: getData(movie, 'runtime'),
               8: getData(movie, 'plot'),
               9: getData(movie, 'country codes'),
               10: getRandomData(movie, 'quotes'),
               11: getData(movie, 'production companies'),
               12: getRandomData(movie, 'trivia'),
               13: getData(movie, 'languages'),
               14: movie.get('rating'),
               15: getData(movie, 'producer')}
    #for i in range(1, 16):
    #    print options[i]
    return options[idx]
    

# Returns imdb data as a readable string for person objects, company objects, etc.
def getData(movie, option):
    output = movie.get(option)
    if output is None:
        return None
    total_data = ''
    for data in output[:-1]:
        total_data += str(data) + ', '
    if not total_data:
        total_data += str(output[-1])
    else:
        total_data += 'and ' + str(output[-1])
    return total_data

def getRandomData(movie, option):
    output = movie.get(option)
    if output is None:
        return None
    random_data = random.choice(output)
    return random_data

def processQuery(option, movie):
    options = [getDirector(movie), getRuntime(movie), getActors(movie), getYear(movie), getFilmRating(movie), getRating(movie)]
    print options[int(option) - 1]



if __name__ == '__main__':
    imdbAccess = IMDb()
    ia = IMDb()
    
    print 'Hi, I\'m Slug MovieBot! I love to talk about all kinds of movies.'
    
    #while True:
    #    questionProcessing(imdbAccess)
    #info = imdbIndex('Transformers', ['director', 'runtime', 'actors', 'year released', 'film rating', 'imdb rating', 
    #                                  'writers', 'languages', 'plot', 'plot outline', 'producers', 'production companies', 
    #                                  'distributors'])
    #for data in info:
    #    print data
    
    #print imdbData('Transformers', 1)
    print imdbData('Zootopia', 12)

    #the_matrix = ia.get_movie('0133093')
    #print the_matrix['director']

    #for person in ia.search_person('Mel Gibson'):
        #print person.personID, person['name']

    # Search for a movie (get a list of Movie objects).
    #s_result = ia.search_movie('The Untouchables')

    # Print the long imdb canonical title and movieID of the results.
    #for item in s_result:
        #print item['long imdb canonical title'], item.movieID

    # Retrieves default information for the first result (a Movie object).
    #the_unt = s_result[0]
    #ia.update(the_unt)

    # Print some information.
    #print the_unt['runtime']
    #print the_unt['rating']
    #director = the_unt['director'] # get a list of Person objects.

    # Get the first item listed as a "goof".
    #ia.update(the_unt, 'goofs')
    #print the_unt['goofs'][0]

    # The first "trivia" for the first director.
    #b_depalma = director[0]
    #ia.update(b_depalma)
    #print b_depalma['trivia'][0]
    #getDirector('Transformers')
    #getRuntime('Transformers')
    