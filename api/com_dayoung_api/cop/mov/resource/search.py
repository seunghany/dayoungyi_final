from flask_restful import Resource, reqparse

from com_dayoung_api.cop.mov.model.movie_dao import MovieDao

class MovieSearch(Resource):
    def get(self, title):
        print('***** MOVIE SEARCH *****')
        movie = MovieDao.find_by_title(title)
        movielist = []
        for d in movie:
            movielist.append(d.json())
        return movielist