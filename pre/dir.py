#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 16 16:31:16 2018

@author: yanyanjiang
"""

from bs4 import BeautifulSoup
import re
import time
import requests
import numpy as np

"""
<div class="col-sm-7 col-xs-16 critic_img"> <img class="critic_thumb fullWidth" src="https://resizing.flixster.com/G-CKTuTqC8Q5g5DAf8VkZ2mvB3c=/72x72/v1.YzszMDE4O2o7MTc4MjM7MjA0ODsxNTAwOzE1MDA" width="50px"> </div>
<div class="col-sm-7 col-xs-16 critic_img"> <img class="critic_thumb fullWidth" src="https://resizing.flixster.com/ptPu_JG_jLVbJacwRCm6GXSC2C4=/72x72/v1.YzsyMjE5O2o7MTc4MzQ7MjA0ODsxMDA7MTAw" width="50px"> </div>

def getImage(review):
    myImage='NA'
    imageChunk=review.find('div',{'class':"col-sm-7 col-xs-16 critic_img"}).img
    if imageChunk: myImage = imageChunk ['src']
    return myImage #'ted lappas'


fresh
<div class="review_icon icon small fresh"></div>

rotten
<div class="review_icon icon small rotten"></div>

def getRating(review):
    myrating = 'NA'
    if review.find('div',{'class':"review_icon icon small fresh"}): myrating = 'fresh'
    if review.find('div',{'class':"review_icon icon small rotten"}): myrating = 'rotten'
    return myrating
    

<em class="subtle">Hollywood Reporter</em>
<em class="subtle">New York Daily News</em>

def getSource(review):
    mysource='NA'       
    sourceChunk=review.find('em',{'class':"subtle"})
    if sourceChunk: mysource=sourceChunk.text
    return mysource


<div class="review_date subtle small"> August 30, 2018</div>
<div class="review_date subtle small"> November 14, 2015</div>

def getDate(review):
    mydate='NA'       
    dataChunk=review.find('div',{'class':"review_date subtle small"})
    if dataChunk: mydate=dataChunk.text
    return mydate


<div class="small subtle"> <a href="http://www.hollywoodreporter.com/review/space-jam-1996-review-947391" target="_blank" rel="nofollow">Full Review</a> </div>

def getLink(review):
    mylink='NA'       
    linkChunk = review.find('div',{'class':"small subtle"}).a
    if linkChunk: mylink=linkChunk['href']
    return mylink


def getDirector(review):
    theDirector = 'NA'
    dierctor = review.find('a',{'href' = "/celebrity/"})
    if director: theDirector = 
    return theDirector
"""
def getdirector_score(director):
    myscore=[]
    director_score = 0
    movie=director.find('div',{'class':re.compile('scrollable-table')})
    scores=movie.findAll('span',{'class':re.compile('tMeterScore')})
    if scores:
        for score in scores:
            score_text=score.text
            myscore.append(score_text)
        myscore=[float(x[:-1]) for x in myscore]
        director_score=np.median(myscore)
        
    return(director_score)

def getdirector_link(movie):
    dirlink="NA"
    mylink=movie.find('a',{'href':re.compile('/celebrity/')})  
    if mylink:
        print("mylink", mylink)
        dirlink=mylink.get('href')
      
   
    return(dirlink)

def run(url):
    
    for i in range(5): # try 5 times
        try:
            #use the browser to access the url
            response=requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })  
            #print(response)
            html=response.content 
            #print(type(html) == type(None))
            
            #if type(html) == type(None):
            if response.status_code != 200:    
                continue 
            else:
                break
            # get the html
            #break # we got the file, break the loop
        except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
            print ('failed attempt')
            time.sleep(2) # wait 2 secs

    if html: # couldnt get the page, ignore
    #print(html)
        soup = BeautifulSoup(html.decode('ascii', 'ignore'),'html.parser') # parse the html
        #print(soup)
        dirlink=getdirector_link(soup)
        if dirlink != 'NA':
            print("dirlink",dirlink)
            director_link="https://www.rottentomatoes.com"+str(dirlink)
        #print(director_link)
            
            for i in range(5): # try 5 times 
                try:
                    #use the browser to access the url
                    response=requests.get(director_link,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', })
                    #print(response)
                    html=response.content # get the html
                    if response.status_code != 200:
                        continue
                    else:
                        break
                     # we got the file, break the loop
                except Exception as e:# browser.open() threw an exception, the attempt to get the response failed
                    print ('failed attempt',i)
                    time.sleep(2)
                
            if html:
                soup = BeautifulSoup(html.decode('ascii', 'ignore'),'html.parser') # parse the html 
                #director_link=getdirector_link(soup)
                director_score = getdirector_score(soup)
                print("score",director_score)
        

"""
    reviews=soup.findAll('div', {'class':re.compile('review_table_row')}) # get all the review divs

    for review in reviews:

        imglink=getImage(review)# finds and returns the name of the critic from the given review object
        
        rating=getRating(review) # finds and returns the rating from the given review object. The return value should be 'rotten' ,  'fresh', or 'NA' if the review doesn't have a rating.

        source=getSource(review) # finds and returns the source (e.g 'New York Daily News') of the review from the given review object. The return value should be 'NA' if the review doesn't have a source.

        date=getDate(review)  ##finds and returns the date of the review from the given review object. The return value should be  'NA' if the review doesn't have a date.

        link=getLink(review) # finds and returns the number of characters in the text of the review from the given review object. The return value should 'NA' if the review doesn't have text.
		
        print(imglink, rating, source, date,link)
 """

if __name__=='__main__':
    #url='https://www.rottentomatoes.com/m/space_jam/reviews/'
#for i in range(0,150):
    f= open('movie_link.txt')
    #for (num,value) in enumerate(f):
    for value in f:
        movies.ix[i,'r']=run(value)
    movies.to_csv("director.txt")


