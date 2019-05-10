#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 12:28:25 2018

@author: thomaslyf
"""

from bs4 import BeautifulSoup
import re
import time
import requests
import pandas as pd
import numpy as np

def getdirector_score(director):
    myscore=[]
    movie=director.find('div',{'class':re.compile('scrollable-table')})
    score=movie.findAll('span',{'class':re.compile('tMeterScore')})
    for score in score:
        score_text=score.text
        myscore.append(score_text)
    myscore=[float(x[:-1]) for x in myscore]
    director_score=np.median(myscore)
    return(director_score)

def getdirector_link(movie):
    dirlink="NA"
    mylink=movie.find('a',{'href':re.compile('/celebrity/')})
    if mylink:
        dirlink=mylink.get('href')
    director_link="https://www.rottentomatoes.com"+str(dirlink)
    return(director_link)

def run(url):
    response=requests.get(url,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', },allow_redirects=False)
    html=response.content # get the html
    soup = BeautifulSoup(html.decode('ascii', 'ignore'),'html.parser') # parse the html 
    director_link=getdirector_link(soup)
    response=requests.get(director_link,headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36', },allow_redirects=False)
    html=response.content # get the html
    soup = BeautifulSoup(html.decode('ascii', 'ignore'),'html.parser') # parse the html 
    director_score=getdirector_score(soup)
    return(director_score)
 
movies = pd.read_csv('movies_link.txt',sep='\n',header=None,names="m")
for i in range(0,8366):
    url=movies.ix[i,'m']
    movies.ix[i,'r']=run(url)
    print (i)
movies.to_csv("director.txt")

