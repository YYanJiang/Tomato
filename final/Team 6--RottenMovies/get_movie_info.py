"""
This file is used to get all the movie information.

For each movie,
1. Get movie name. Note: movie names have two forms.
2. Get critic score, in the form of percent.
3. Get audience score, in the form of percent.
4. Get rating.
5. Get genres, for each movie, may have multiple genres.
6. For the master director, get the director score(median).
7. For the master writer, get the writer score(median).
8. Get the date for launch time in theater, and whether the movie is available only in the theater or not.
9. Get the date for launch time on disc/streaming.
10. Get the box office.
11. Get the runtime.
12. Get the studio.
13. For the first four casts, get the cast score (the median).
"""

from bs4 import BeautifulSoup
import re
import time
import requests
import numpy as np
import codecs

def get_movie_name(movie):
    """ return movie name """
    name = 'NA'
    ilinkChunk = movie.find('h1', {'class': re.compile("title hidden-xs")})
    if ilinkChunk: name = ilinkChunk.text
    else:
        nameChunk = movie.find('h1', {'id': re.compile('movie-title')})
        if nameChunk: name = nameChunk.text
    return name.strip()

def get_critic_score(movie):
    """ return critic score """
    source = 'NA'
    sourceChunk = movie.find('span', {'class': re.compile('meter-value')})
    if sourceChunk: source = sourceChunk.text
    return source

def get_audience_score(movie):
    """ return audience score """
    score = 'NA'
    scoreChunk = movie.find('span', {'style': re.compile('vertical-align:top')})
    if scoreChunk: score = scoreChunk.text
    return score

def get_rating(movie):
    """ return rating """
    rating = 'NA'
    ratingChunk = movie.find('div', {'class': re.compile('meta-value')})
    if ratingChunk: rating = ratingChunk.text
    return rating

def get_genre(movie):
    """ return genres """
    genre = ''
    genreChunk = movie.findAll('a', {'href': re.compile('genres')})
    for g in genreChunk:
        if not g:
            return 'NA'
        else:
            genre += g.text.strip() + ','
    return genre.strip(',')

def get_theater_date(movie):
    """ return in theater datetime """
    date = 'NA'
    dateChunk = movie.find('time')
    if dateChunk: date = dateChunk.text

    l = movie.find('span') # verify a movie is limited to theater or not
    if l: date += l.text

    return date

def get_streaming_date(movie):
    """ return streaming datetime """
    date = 'NA'
    dateChunk = movie.find('time')
    if dateChunk: date = dateChunk.text
    return date

def get_box_office(movie):
    """ return box office """
    box_office = 'NA'
    boxofficeChunk = movie.find('div', {'class': re.compile('meta-value')})
    if boxofficeChunk: box_office = boxofficeChunk.text
    return box_office

def get_runtime(movie):
    """ return runtime """
    time = 'NA'
    timeChunk = movie.find('time', {'datetime': re.compile('M')})
    if timeChunk: time = timeChunk.text
    return time.strip()

def get_studio(movie):
    """ return studio """
    studio = 'NA'
    studioChunk = movie.find('a', {'target': re.compile('movie-studio')})
    if studioChunk: studio = studioChunk.text
    return studio

def get_link(movie):
    """ return the link for director/ writer/ cast """
    link='NA'
    linkChunk = movie.find('a',{'href':re.compile('/celebrity/')})
    if linkChunk:
        link = 'https://www.rottentomatoes.com' + linkChunk.get('href')
    return  link

def get_score(movie):
    """ return the median score for each person """
    link = get_link(movie)
    soup = run(link)
    if soup == 'NA': return 'NA' # some casts' link would return 404 Not Found Error

    all_score = []
    scores = soup.find('div',{'class':re.compile('scrollable-table')})

    if scores:
        score = scores.findAll('span', {'class': re.compile('tMeterScore')})

        for s in score:
            all_score.append(s.text)

        all_score = [float(x[:-1]) for x in all_score]
        person_score = np.median(all_score)
        return(str(person_score))
    else:
        return 'NA'

def get_cast_score(movie):
    """ return the first four casts score """
    casts = movie.findAll('div', {'class': re.compile('cast-item media')})
    actor_score = ''

    if len(casts) == 0:  # no cast found
        return 'NA'
    elif len(casts) <= 4:  # less then 4 casts found, then return all the casts score
        casts_score = [get_score(c) for c in casts]
    else:  # get the first 4 casts score
        casts_score = [get_score(c) for c in casts[0:4]]

    for s in casts_score:
        actor_score += str(s) + ','

    return actor_score.strip(',')

def run(url):
    """ run the url, return parsed html """
    html = None
    for counter in range(11): # give 10 tries
        if counter == 10: # after 10 tries, return no information
            return 'NA'

        try:
            # use the browser to access the url
            response = requests.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            if response: # in case response is 404 Not Found Error
                html = response.content  # get the html
                if type(html) == type(None): # in case nothing get from the html
                    print("Error!")
                    continue
                break
            else:
                continue

        except Exception as e:  # browser.open() threw an exception, the attempt to get the response failed
            print('failed attempt')
            time.sleep(2)  # wait 2 secs

    soup = BeautifulSoup(html.decode('ascii', 'ignore'), 'html.parser')  # parse the html
    return soup

def get_all_info(url):
    """ return all the info for the given movie link """
    movie = run(url)
    if movie == 'NA': return 'NA'

    elements = movie.findAll('li', {'class': re.compile('meta-row clearfix')})

    name = get_movie_name(movie)
    critic_score = get_critic_score(movie)
    audience_score = get_audience_score(movie)

    rating = theater_date = genres = director_score = writer_score = streaming_date = box_office = runtime = studio = 'NA'
    for item in elements:
        title = item.find('div', {'class': re.compile('meta-label subtle')}).text
        if title == 'Rating: ':
            rating = get_rating(item)
        elif title == 'Genre: ':
            genres = get_genre(item)
        elif title == 'Directed By: ':
            director_score = get_score(item)
        elif title == 'Written By: ':
            writer_score = get_score(item)
        elif title == 'In Theaters: ':
            theater_date = get_theater_date(item)
        elif title == 'On Disc/Streaming: ':
            streaming_date = get_streaming_date(item)
        elif title == 'Box Office: ':
            box_office = get_box_office(item)
        elif title == 'Runtime: ':
            runtime = get_runtime(item)
        elif title == 'Studio: ':
            studio = get_studio(item)

    actor_score = get_cast_score(movie)

    print(name, critic_score, audience_score, rating, genres, director_score, writer_score, actor_score, theater_date, streaming_date, box_office, runtime, studio)    # # print(director_score, writer_score, actor_score)
    print('\n')

    return name + '\t' + critic_score + '\t' + audience_score + '\t' + rating + '\t' + genres + '\t' + director_score + '\t' + writer_score + '\t' + actor_score + '\t' + theater_date + '\t' + streaming_date + '\t' + box_office + '\t' + runtime + '\t' + studio

if __name__ == '__main__':
    url1 = 'https://www.rottentomatoes.com/m/lassie_come_home'
    url2 = 'https://www.rottentomatoes.com/m/the_lego_movie'
    url3 = 'https://www.rottentomatoes.com/m/war_machine_2016'
    url4 = 'https://www.rottentomatoes.com/m/firehouse_dog'
    url5 = 'https://www.rottentomatoes.com/m/in_the_blood_2013'
    url6 = 'https://www.rottentomatoes.com/m/la_nouvelle_guerre_des_boutons'
    url7 = 'https://www.rottentomatoes.com/m/paradise_lost_3_purgatory_2009'
    url8 = 'https://www.rottentomatoes.com/m/jupiter_ascending_2014'
    url9 = 'https://www.rottentomatoes.com/m/wild_one'
    
#    get_all_info(url9)
#    movies = list()
#    l = [url1, url2, url3, url4, url5, url6, url7, url8, url9]
#    for m in l:
#        movie = get_all_info(m)
#        movies.append(movie)

    movies = list()

    file = open('movie_link.txt')
    with file:
        for line in file:
            movie = get_all_info(line)
            movies.append(movie)
    file.close()

    # writing the set entries to movie file
    try:
        o_file = codecs.open('movie_info.txt', 'w',"utf-8") # output file 
        o_file.write('name' + '\t' + 'critic-score' +'\t' + 'audience-score' + '\t' + 'rating' + '\t' + 'genres' + '\t' + 'director_score' + '\t' + 'writer_score' + '\t' + 'actor_score' + '\t' + 'theater-date' + '\t' + 'streaming-date' + '\t' + 'box-office' + '\t' + 'runtime' + '\t' + 'studio' + '\n')
        for x in movies:
            o_file.write(x + '\n')
        o_file.close()

    except:
        print("Error while trying to create movie_info.txt file")