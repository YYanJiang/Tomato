from bs4 import BeautifulSoup
import re
import time
import requests
import numpy as np

def getMovieName(movie):
    name = 'NA'
    ilinkChunk = movie.find('h1', {'class': re.compile("title hidden-xs")})
    if ilinkChunk: name = ilinkChunk.text
    else:
        nameChunk = movie.find('h1', {'id': re.compile('movie-title')})
        if nameChunk: name = nameChunk.text
    return name.strip()

def getCriticScore(movie):
    source = 'NA'
    sourceChunk = movie.find('span', {'class': re.compile('meter-value')})
    if sourceChunk: source = sourceChunk.text

    return source

def getAudienceScore(movie):
    score = 'NA'
    scoreChunk = movie.find('span', {'style': re.compile('vertical-align:top')})
    if scoreChunk: score = scoreChunk.text
    return score

def getRating(movie):
    rating = 'NA'
    ratingChunk = movie.find('div', {'class': re.compile('meta-value')})
    if ratingChunk: rating = ratingChunk.text
    return rating

def getGenre(movie):
    genre = ''
    genreChunk = movie.findAll('a', {'href': re.compile('genres')})
    for g in genreChunk:
        if not g:
            return 'NA'
        else:
            genre += g.text.strip() + ','
    return genre.strip(',')

def getInTheaterDate(movie):
    date = 'NA'
    dateChunk = movie.find('time')
    if dateChunk: date = dateChunk.text

    l = movie.find('span')
    if l: date += l.text

    return date

def getStreamingDate(movie):
    date = 'NA'
    dateChunk = movie.find('time')
    if dateChunk: date = dateChunk.text
    return date

def getBoxOffice(movie):
    boxoffice = 'NA'
    boxofficeChunk = movie.find('div', {'class': re.compile('meta-value')})
    if boxofficeChunk: boxoffice = boxofficeChunk.text
    return boxoffice

def getRunTime(movie):
    # Some movies has no runtime.
    time = 'NA'
    timeChunk = movie.find('time', {'datetime': re.compile('M')})
    if timeChunk: time = timeChunk.text
    return time.strip()

def getStudio(movie):
    studio = 'NA'
    studioChunk = movie.find('a', {'target': re.compile('movie-studio')})
    if studioChunk: studio = studioChunk.text
    return studio

def get_score(people_link):
    """
    html=None
    for i in range(5):
             try:
                 response=requests.get(people_link,headers =headers)
                 html=response.content # get the html
                 break # we got the file, break the loop
             except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                 time.sleep(2) # wait 2 secs
    if not html: return("NA")
    else:
       
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'html.parser') # parse the html
      """  
    myscore=[]
    movie = run(people_link)
    score_table = movie.find('div',{'class':re.compile('scrollable-table')})   
    if score_table:
        score=score_table.findAll('span',{'class':re.compile('tMeterScore')})
        for score in score:
            score_text=score.text
            myscore.append(score_text)
        myscore=[float(x[:-1]) for x in myscore]
        people_score=np.median(myscore)
        return(people_score)
    else:
        return("NA")

def get_link(movie):
    dirlink="NA"
    mylink=movie.find('a',{'href':re.compile('/celebrity/')})
    if mylink:
        dirlink=mylink.get('href')
    director_link="https://www.rottentomatoes.com"+str(dirlink)
    return(director_link)

def run(url):
    html = None
    for counter in range(10):
        if counter == 9:
            return 'NA' + '\t' + 'NA' + '\t' + 'NA' + '\t' + 'NA' + '\t' + 'NA' + '\t' + 'NA' + '\t' + 'NA' + '\t' + 'NA' + '\t' + 'NA' + '\t' + 'NA'
        try:
            # use the browser to access the url
            response = requests.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
            if response:
                html = response.content  # get the html
                if type(html) == type(None):
                    print("Error!")
                    continue
                break
            else:
                continue
        except Exception as e:  # browser.open() threw an exception, the attempt to get the response failed
            print('failed attempt')
            time.sleep(2)  # wait 2 secs
    movie = BeautifulSoup(html.decode('ascii', 'ignore'), 'html.parser')  # parse the html
    
    return(movie)

if __name__ == '__main__':
    url1 = 'https://www.rottentomatoes.com/m/lassie_come_home'
    url2 = 'https://www.rottentomatoes.com/m/the_lego_movie'
    url3 = 'https://www.rottentomatoes.com/m/war_machine_2016'
    # run(url3)
    url4 = 'https://www.rottentomatoes.com/m/firehouse_dog'
    url5 = 'https://www.rottentomatoes.com/m/in_the_blood_2013'
    # run(url4)
    # run(url5)

    url6 = 'https://www.rottentomatoes.com/m/la_nouvelle_guerre_des_boutons'
    #run(url6)
    
    movie = run(url6)
    
    name = getMovieName(movie)
    critic_score = getCriticScore(movie)
    audience_score = getAudienceScore(movie)

    rating  = genres = director_score = writer_score = theater_date = streaming_date = box_office = runtime = studio = 'NA'
    elements = movie.findAll('li', {'class': re.compile('meta-row clearfix')})
    
    for item in elements:
        title = item.find('div', {'class': re.compile('meta-label subtle')}).text
        if title == 'Rating: ':
            rating = getRating(item)
            print(rating)
        elif title == 'Genre: ':
            genres = getGenre(item)
            print(genres)
        elif title == 'Directed By: ':
            director_score = get_score(get_link(item))
            print(director_score)
        elif title == 'Written By: ': 
            writer_score = get_score(get_link(item))
            print(writer_score)
        elif title == 'In Theaters: ':
            theater_date = getInTheaterDate(item)
            print(theater_date)
        elif title == 'On Disc/Streaming: ':
            streaming_date = getStreamingDate(item)
            print(streaming_date)
        elif title == 'Box Office: ':
            box_office = getBoxOffice(item)
            print(box_office)
        elif title == 'Runtime: ':
            runtime = getRunTime(item)
            print(runtime)
        elif title == 'Studio: ':
            studio = getStudio(item)
            print(studio)


    actor_info = movie.findAll('div', {'class': re.compile('cast-item media')})
    actor_score = ''
    actor_link = []
    if len(actor_info) < 3:
        for i in range(len(actor_info)):        
            actor_link.append(get_link(actor_info[i]))
            actor_score += str( get_score(actor_link[i]))
    else:
        for i in range(3):        
            actor_link.append(get_link(actor_info[i]))
            actor_score += str( get_score(actor_link[i]))
    print(actor_score)
    
     
    print(name, critic_score, audience_score, rating, genres, theater_date, streaming_date, box_office, runtime, studio)
    print(director_score, writer_score, actor_score)
    print('\n')
    
    
    

"""    

    #director = elements[2]
    #writer = elements[3]

    #director_link = get_link(director)
    #director_score = get_score(director_link)
    #print(director_score)

    #writer_link = get_link(writer)
    #writer_score = get_score(writer_link)
    #print(writer_score)
    
    
        # actor1_score = "NA"
        # actor2_score = "NA"
        # actor3_score = "NA"
        # return (director_score, writer_score, actor1_score, actor2_score, actor3_score)
        
        
        actor1 = actor_info[0]
        actor2 = actor_info[1]
        actor3 = actor_info[2]
        actor1_link = get_link(actor1)
        actor2_link = get_link(actor2)
        actor3_link = get_link(actor3)
        actor_score += get_score(actor1_link)
        actor_score += get_score(actor2_link)
        actor_score += get_score(actor3_link)



    # return name + '\t' + critic_score + '\t' + audience_score + '\t' + rating + '\t' + genres + '\t' + theater_date + '\t' + streaming_date + '\t' + box_office + '\t' + runtime + '\t' + studio


if __name__ == '__main__':
    

    url1 = 'https://www.rottentomatoes.com/m/lassie_come_home'
    url2 = 'https://www.rottentomatoes.com/m/the_lego_movie'
    url3 = 'https://www.rottentomatoes.com/m/war_machine_2016'
    # run(url3)
    url4 = 'https://www.rottentomatoes.com/m/firehouse_dog'
    url5 = 'https://www.rottentomatoes.com/m/in_the_blood_2013'
    # run(url4)
    # run(url5)

    url6 = 'https://www.rottentomatoes.com/m/la_nouvelle_guerre_des_boutons'
    run(url6)

    # movies = list()
    # l = [url1, url2, url3, url4, url5, url6]
    # for m in l:
    #     movie = run(m)
    #     movies.append(movie)

    # movies = list()
    #
    # file = open('movie_link_action.txt')
    # with file:
    #     for line in file:
    #         movie = run(line)
    #         movies.append(movie)
    # file.close()

    # writing the set entries to movie file
    # try:
    #     o_file = open('action_movie_info.txt', 'w')  # output file
    #
    #     o_file.write('name' + '\t' + 'critic-score' +'\t' + 'audience-score' + '\t' + 'rating' + '\t' + 'genres' + '\t' + 'theater-date' + '\t' + 'streaming-date' + '\t' + 'box-office' + '\t' + 'runtime' + '\t' + 'studio' + '\n')
    #
    #     for x in movies:
    #         print(x)
    #         o_file.write(x + '\n')
    #
    # except:
    #     print("Error while trying to create action_movie_info.txt file")
"""