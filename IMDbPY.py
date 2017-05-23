'''

@author: alifsarker
'''

from imdb import IMDb

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
    if s_result is None:
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

def processQuery(option, movie):
    options = [getDirector(movie), getRuntime(movie), getActors(movie), getYear(movie), getFilmRating(movie), getRating(movie)]
    print options[int(option) - 1]



if __name__ == '__main__':
    imdbAccess = IMDb()
    ia = IMDb()
    
    print 'Hi, I\'m Slug MovieBot! I love to talk about all kinds of movies.'
    
    while True:
        questionProcessing(imdbAccess)

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
    