# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse

import json
# Create your views here.

#APIAI lib
import apiai
import sys, json, requests

import imdb
import collections

import logging

import urllib
import urllib2
from bs4 import BeautifulSoup


def start(request):
    resp = {}

    if 'msg' in request.GET:
        message = request.GET['msg']
        #    logger.info('Handling request :%s', message)
        print 'Handling request : ', message
    else:
        resp['State']="ERROR"
        resp['Content'] = ""
        resp['Input'] = ""
        #    logger.info('Handling request : Error No Message in request')
        print 'Handling request : Error No Message in request'
        return HttpResponse(json.dumps(resp), content_type="application/json")

    mBud = apiai.ApiAI("e96bdf708e17472e89a54e275c67e690")
    def getIntent(msg,i):
        #    logger.info('Intent handling :%s', msg)
        request = mBud.text_request()
        request.query = msg
        request.contexts.append(i)

        # Receiving the response.
        response = json.loads(request.getresponse().read().decode('utf-8'))
        responseStatus = response['status']['code']
        
        
        if (responseStatus == 200):
            # Sending the textual response of the bot.
            #   logger.info('Intent predicted :%s', response['result']['fulfillment']['speech'])
            print 'Intent handling : Intent predicted : ', response['result']['fulfillment']['speech']
            return response['result']['fulfillment']['speech']
        else:
            #   logger.info('No response here from DialogFlow')
            print 'No response here from DialogFlow'
            return -1
        pass
    intent = getIntent(message,"question")
    #print(intent)
    def askAgain():
        print 'Did not here it correct'
        #    logger.info('Did not here it correct')
        resp['State'] = "InternalError"
        resp['Content'] = ""
        resp['Input'] = ""


    def similarMod():
        #    logger.info('Similar Movie Question')
        resp['State'] = "Quest"
        resp['Content'] = "Ok, and what is your favourite movie ?"
        resp['Input'] = ""
        print 'Similar Movie Question : Similar search question : ',resp['State'],resp['Content'],resp['Input']
        # logger.info('Similar Movie Question : Similar search question :%s',resp['Content'])

    def genreMod():
        #    logger.info('Genre Question')
        resp['State'] = "Quest"
        resp['Content'] = "Yes sure and what is your favourite genre"
        resp['Input'] = ""
        print 'Genre Question : Genre search question : ',resp['State'],resp['Content'],resp['Input']
        #    logger.info('Genre Question : Genre search question :%s,%s,%s',resp['State'],resp['Content'],resp['Input'])

    def exactMod():
        #    logger.info('Exact Movie Question')
        resp['State'] = "Quest"
        resp['Content'] = "Great and which movie would you like to watch"
        resp['Input'] = ""
        print 'Exact Movie Question : Exact movie search question : ',resp['State'],resp['Content'],resp['Input']
        #    logger.info('Exact Movie Question : Exact movie search question :%s,%s,%s',resp['State'],resp['Content'],resp['Input'])

    def searchGenre(genre):
        #    logger.info('Genre searched')
        movie = collections.defaultdict(str)
        movie['Horror']='The Cabinet of Dr. Caligari \n Get Out \n Psycho \n The Cabin in the Woods'
        movie['Comedy']='Sideways \n School of Rock \n Lost in Translation \n The Grand Budapest Hotel'
        movie['Romantic'] = 'It Happened One Night \n Singin in the Rain \n Casablanca \n The Big Sick'
        movie['Drama'] = 'Citizen Kane \n All About Eve \n Metropolis \n The Godfather \n Moonlight'
        movie['Crime'] = 'The Godfather \n The Godfather: Part II \n Pulp Fiction \n The Dark Knight \n Kill Bill: Vol. 1 \n The Departed'
        movie['Adventure'] = 'Journey to the Center of the Earth \n The Goonies  \n Everest \n Jurassic World'
        movie['Classics'] = 'The Wizard of Oz \n Citizen Kane \n The Third Man \n The Cabinet of Dr. Caligari (Das Cabinet des Dr. Caligari) \n All About Eve \n Metropolis'
        movie['Animated'] = 'Inside Out \n Snow White and the Seven Dwarfs \n Zootopia \n Toy Story 3 \n Toy Story 2 \n Up'
        movie['Sci-Fi'] = 'The Wizard of Oz \n Mad Max: Fury Road \n Metropolis \n E.T. The Extra-Terrestrial \n Wonder Woman'
        movie['Top'] = 'The Wizard of Oz \n Citizen Kane \n The Third Man \n Get Out \n Mad Max: Fury Road \n The Cabinet of Dr. Caligari \n All About Eve'
        movie['Latest'] = 'Star Wars: The Last Jedi \n Wonder \n Justice League \n The star \n The man who invented christmas'
        resp['State'] = "Genre"
        resp['Content'] = movie[genre]
        resp['Input'] = genre
        print 'Genre searched : Genre search result : ',resp['State'],resp['Content'],resp['Input']
        #    logger.info('Genre searched : Genre search result :%s,%s,%s',resp['State'],resp['Content'],resp['Input'])
        
    def getSynopsis(movie):
        imdb_object,mName = searchMovie(movie,2)
        resp['State'] = "Synopsis"
        resp['Content'] = mName.get('plot outline')
        resp['Input'] = movie
        print 'Synopsis asked result : ',resp['State'],resp['Content'],resp['Input']

    def likeMovie(movie):
        #    logger.info('Similar Movie searched : %s',movie)
        #imdb_object = imdb.IMDb('http')
        imdb_object,mName = searchMovie(movie,2)
        src = requests.get(imdb_object.get_imdbURL(mName)).text
        bs = BeautifulSoup(src, "lxml")
        recs = [rec['data-tconst'][2:] for rec in bs.findAll('div', 'rec_item')][:3]
        resp['State'] = 'Similar'
        sim = ''
        for rec in recs:
            mov = imdb_object.get_movie(rec)
            #print(mov['title'])
            sim+= (mov['title'] + '\n')
        #print movie['title']
        resp['Content'] = sim.strip('\n')
        resp['Input'] = movie
        print 'Similar Movie searched : Similar Movie search list : ',resp['State'],resp['Content'],resp['Input']
        #    logger.info('Similar Movie searched : Similar Movie search list :%s,%s,%s',resp['State'],resp['Content'],resp['Input'])

    def searchMovie(mName,k=1):
        #    logger.info('Exact Movie searched : %s',mName)
        imdb_object = imdb.IMDb('http')
        mSearch = imdb_object.search_movie(mName)
        if k!=1:
            return imdb_object,mSearch[3]
        #mSearch.sort()
        res = set()
        resp['State'] = 'Exact'
        for mov in mSearch[:5]:
            res.add(mov['title'])
        resp['Content'] = '\n'.join(list(res))
        resp['Input'] = mName
        print 'Exact Movie searched : Exact Movie search list : ',resp['State'],resp['Content'],resp['Input']
        #    logger.info('Exact Movie searched : Exact Movie search list :%s,%s,%s',resp['State'],resp['Content'],resp['Input'])
        
    
    def youtubeLink(mName):
        #    logger.info('Youtube Video searched :%s',mName)
        searchMovie(mName)
        textToSearch = mName + ' official trailer'
        query = urllib.quote(textToSearch)
        url = "https://www.youtube.com/results?search_query=" + query+"&sp=EgIQBFAU"
        response = urllib2.urlopen(url)
        html = response.read()
        soup = BeautifulSoup(html,"lxml")
        vid = soup.findAll(attrs={'class':'yt-uix-tile-link'})[0]
        
        resp['State'] = "Video"
        resp['Content'] = 'https://www.youtube.com' + vid['href']
        resp['Input'] = mName
        print 'Youtube Video searched : Youtube link search result : ',resp['State'],resp['Content'],resp['Input']
        #    logger.info('Youtube Video searched : Youtube link search result :%s,%s,%s',resp['State'],resp['Content'],resp['Input'])
        
    def help():
        print 'Help Asked'
        #    logger.info('Did not here it correct')
        resp['State'] = "Help"
        resp['Content'] = ""
        resp['Input'] = ""
        
        
    if intent=="Similar":
        similarMod()
    elif intent=="Genre":
        genreMod()
    elif intent=="movies":
        exactMod()
    elif intent=="help":
        help()
    elif intent and intent[0]=='1':
        searchGenre(intent[2:])
    elif intent and intent[0]=='2':
        searchMovie(intent[2:])
    elif intent and intent[0]=='3':
        likeMovie(intent[2:])
    elif intent and intent[0]=='4':
        youtubeLink(intent[2:])
    else:
        askAgain()
        
    return HttpResponse(json.dumps(resp), content_type="application/json")
        
        
        
        
        
        
        
        
        
        
        
        
