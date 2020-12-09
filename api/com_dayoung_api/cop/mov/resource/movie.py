from flask import request, jsonify
from flask_restful import Resource, reqparse

from com_dayoung_api.cop.mov.model.movie_dao import MovieDao
from com_dayoung_api.cop.mov.model.movie_dto import MovieDto

parser = reqparse.RequestParser()

class Movie(Resource):
    @staticmethod
    def post():
        print('***** MOVIE REGISTER *****')
        parser.add_argument('mov_id', type=int, required=False, help='This field should be a movieid')
        parser.add_argument('title_kor', type=str, required=True, help='This field should be a title_kor')
        parser.add_argument('title_naver_eng', type=str, required=True, help='This field should be a title_naver_eng')
        parser.add_argument('genres_kor', type=str, required=True, help='This field should be a genres_kor')
        parser.add_argument('keyword_kor', type=str, required=True, help='This field should be a keyword_kor')
        parser.add_argument('running_time_kor', type=int, required=True, help='This field should be a running_time_kor')
        parser.add_argument('year_kor', type=str, required=True, help='This field should be a year_kor')
        parser.add_argument('director_naver_kor', type=str, required=True, help='This field should be a director_naver_kor')
        parser.add_argument('actor_naver_kor', type=str, required=True, help='This field should be a actor_naver_kor')
        parser.add_argument('movie_l_rating', type=float, required=True, help='This field should be a movie_l_rating')
        parser.add_argument('movie_l_rating_count', type=int, required=True, help='This field should be a movie_l_rating_count')
        parser.add_argument('movie_l_popularity', type=float, required=True, help='This field should be a movie_l_popularity')
        parser.add_argument('link_naver', type=str, required=True, help='This field should be a link_naver')
        parser.add_argument('image_naver', type=str, required=True, help='This field should be a image_naver')              
        args = parser.parse_args()
        try:
            MovieDao.register_movie(args)
            return{'code':0, 'message':'SUCCESS'}, 200
        except:
            return {'message':'An error occured registering the movie'}, 500

    @staticmethod
    def put():
        print('***** MOVIE UPDATE *****')
        parser.add_argument('mov_id', type=int, required=True, help='This field should be a movieid')
        parser.add_argument('title_kor', type=str, required=True, help='This field should be a title_kor')
        parser.add_argument('title_naver_eng', type=str, required=True, help='This field should be a title_naver_eng')
        parser.add_argument('genres_kor', type=str, required=True, help='This field should be a genres_kor')
        parser.add_argument('keyword_kor', type=str, required=True, help='This field should be a keyword_kor')
        parser.add_argument('running_time_kor', type=int, required=True, help='This field should be a running_time_kor')
        parser.add_argument('year_kor', type=str, required=True, help='This field should be a year_kor')
        parser.add_argument('director_naver_kor', type=str, required=True, help='This field should be a director_naver_kor')
        parser.add_argument('actor_naver_kor', type=str, required=True, help='This field should be a actor_naver_kor')
        parser.add_argument('movie_l_rating', type=float, required=True, help='This field should be a movie_l_rating')
        parser.add_argument('movie_l_rating_count', type=int, required=True, help='This field should be a movie_l_rating_count')
        parser.add_argument('movie_l_popularity', type=float, required=True, help='This field should be a movie_l_popularity')
        parser.add_argument('link_naver', type=str, required=True, help='This field should be a link_naver')
        parser.add_argument('image_naver', type=str, required=True, help='This field should be a image_naver')         
        args = parser.parse_args()
        movies = MovieDto(args['mov_id'], \
                        args['title_kor'], \
                        args['title_naver_eng'], \
                        args['genres_kor'], \
                        args['keyword_kor'], \
                        args['running_time_kor'], \
                        args['year_kor'], \
                        args['director_naver_kor'], \
                        args['actor_naver_kor'], \
                        args['movie_l_rating'], \
                        args['movie_l_rating_count'], \
                        args['movie_l_popularity'], \
                        args['link_naver'], \
                        args['image_naver'])
        try:
            MovieDao.modify_movie(args)
            return{'code':0, 'message':'SUCCESS'}, 200
        except:
            return {'message':'An error occured modifying the movie'}, 500
            
    @staticmethod
    def delete(mov_id):
        print('***** MOVIE DELETE *****')
        movie = MovieDao.find_by_id(mov_id) # Primary Key로 삭제하려는 리뷰의 Row를 불러옴.
        try:
            MovieDao.delete_movie(movie.mov_id) # 해당 리뷰를 데이터베이스에서 삭제
            return{'code':0, 'message':'SUCCESS'}, 200
        except:
            return {'message':'An error occured deleting the movie'}, 500

class Movies(Resource):
    @staticmethod
    def post():
        print('***** MOVIE DB INSERT *****')
        rmd = MovieDao()
        rmd.bulk()

    @staticmethod
    def get():
        print('***** MOVIE ALL LIST RANDOM *****')
        data = MovieDao.find_all_sort_random()
        return data, 200        

