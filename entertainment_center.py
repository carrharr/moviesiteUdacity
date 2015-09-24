#!/usr/bin/python

import fresh_tomatoes
import media
import requests
import json
import config

# Youtube base url and api key
youtubeKey = ""
ytUrl = "https://www.youtube.com/watch?v="

# Movie List for display on html
# Add movies to movieList as < ,"Movie Name" > ,excluding < & >
# Please keep indentation
movieList = ["Eyes Wide Shut", "A Clockwork Orange", "Legends of the Fall",
            "The Godfather", "Blade Runner", "Her", "Scarface", "Inception",
            "Se7en", "The Walking Dead"]
movies = []

# Function for retrieving info from movie names
def getInfo(video):
    # Youtube request
    yt = requests.get('https://www.googleapis.com/youtube/v3/search?part=s'
                           'nippet&q=' + video + 'trailer&maxResults=1&key=' +
                           youtubeKey, timeout=20)
    ytStr = yt.text
    ytDict = json.loads(ytStr)
    vidId = ytDict['items'][0]['id']['videoId']
    vidUrl = ytUrl + vidId

    # Open Movie Database request
    res = requests.get('http://www.omdbapi.com/?t=' + video + '&y=&plot='
                          'short&r=json', timeout=20)
    resStr = res.text
    # Set dictionary values for fresh tomatoes display from Youtube and OMDB
    # json's
    response = json.loads(resStr)

    trailer_youtube_url = vidUrl
    movie_title = response["Title"]
    poster_image = response["Poster"]
    movie_storyline = response["Plot"]
    rating = response["Metascore"]
    genre = response["Genre"]
    date = response["Released"]
    director = response["Director"]
    actors = response["Actors"]

    movies.append(media.Movie(movie_title, movie_storyline, poster_image,
                            trailer_youtube_url, rating, genre, director,
                             date, actors))

    # Check all variables are correct!!!!
    print movie_title + " OK"


for Movie in movieList:
    try:
        getInfo(Movie)
    except:
        print "failed to get data "


fresh_tomatoes.open_movies_page(movies)
