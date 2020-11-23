#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#

import sys
# importing the requests library 
import requests
import random
import re


genres = {
    "acao": 28,
    "aventura": 12,
    "animacao": 16,
    "comedia": 35,
    "policial": 80,
    "documentario": 99,
    "drama": 18,
    "familia": 10751,
    "fantasia": 14,
    "historia": 36,
    "terror": 27,
    "musical": 10402,
    "romance": 10749,
    "ficcao cientifica": 878,
    "suspense": 53,
    "guerra": 10752,
    "faroeste": 37
}

personSend = {
    "query" : ""
}

movieDb = {
 
}

movieSend = {
}


def remove_accents(string):
    string = re.sub(u"[àáâãäå]", 'a', string)
    string = re.sub(u"[èéêë]", 'e', string)
    string = re.sub(u"[ìíîï]", 'i', string)
    string = re.sub(u"[òóôõö]", 'o', string)
    string = re.sub(u"[ùúûü]", 'u', string)
    string = re.sub(u"[ýÿ]", 'y', string)
    string = re.sub(u"[ç]", 'c', string)

    return string


def main(dict):
    # api-endpoint

    
    linkAfter = "/similar?api_key=094fd8f84048425f068f6965ca8bb6af&language=pt-BR"
    linkBefore = "https://api.themoviedb.org/3/movie/"
    
    chosen = random.choice(list(dict.keys()))
    
    
    if(chosen == 'actor' or chosen == 'director'):
        personSend['query'] = dict[chosen]
        URL_person ="https://api.themoviedb.org/3/search/person?api_key=094fd8f84048425f068f6965ca8bb6af&language=pt-BR" 
        # sending get request for actor and saving the response as response object 
        s = requests.get(url = URL_person, params = personSend )
        dataPerson = s.json()
        movieDb['with_people'] = [dataPerson['results'][0]['id']]
    
        
    if(chosen == 'movie'):
        movieSend['query'] = dict[chosen]
        URL_movie ="https://api.themoviedb.org/3/search/movie?api_key=094fd8f84048425f068f6965ca8bb6af&language=pt-BR" 
        # sending get request for actor and saving the response as response object 
        m = requests.get(url = URL_movie, params = movieSend )
        dataRelatedMovies = m.json()
        referenceMovieId = dataRelatedMovies['results'][0]['id']
        URLmovie = linkBefore + str(referenceMovieId) + linkAfter
        m = requests.get(url = URLmovie)
        dataRelatedMovies = m.json()
        sizeM = len(dataRelatedMovies['results'])
        number = random.randint(0, sizeM-1)
        return dataRelatedMovies['results'][number]
        
    if(chosen == 'genre'):
        genre = dict['genre']
        genre = genre.lower()
        genre = remove_accents(genre)
        movieDb['with_genres'] = genres[genre]
        
    
    
    URL = "https://api.themoviedb.org/3/discover/movie?api_key=094fd8f84048425f068f6965ca8bb6af&language=pt-BR"
    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = movieDb) 
    
      
    # extracting data in json format 
    data = r.json() 
    
    size = len(data['results'])
    
    number = random.randint(0, size-1)
    
    return data['results'][number]