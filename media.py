#!/usr/bin/python

#Create class movie for usage in entertainment center

class Movie():
    def __init__(self, movie_title, movie_storyline, poster_image,
                trailer_youtube_url, rating, genre, director, date,
                actors):
        self.title = movie_title
        self.storyline = movie_storyline
        self.posterImageUrl = poster_image
        self.trailerYoutubeUrl = trailer_youtube_url
        self.rating = rating
        self.genre = genre
        self.date = date
        self.director = director
        self.actors = actors
