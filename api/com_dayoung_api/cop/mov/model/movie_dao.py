from typing import List
import json
import pandas as pd
import os
import sys
import urllib.request
import csv
import ast
import time
from pandas import DataFrame
from pathlib import Path

from flask import request, jsonify
from flask_restful import Resource, reqparse

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import func

from com_dayoung_api.ext.db import db, openSession

from com_dayoung_api.cop.mov.model.movie_dto import MovieDto
from com_dayoung_api.cop.mov.model.movie_dfo import MovieDfo

Session = openSession()
session = Session()

class MovieDao(MovieDto):
    
    @staticmethod
    def bulk():
        print('***** INSERT MOVIE DF *****')
        recomoviedf = MovieDfo()
        df = recomoviedf.hook()
        print(df)
        session.bulk_insert_mappings(MovieDto, df.to_dict(orient='records'))
        session.commit()
        session.close()
        print('***** INSERT MOVIE DF COMPLETE *****')

    @staticmethod
    def count():
        return session.query(func.count(MovieDto.mov_id)).one()
    
    @staticmethod
    def find_by_title(title):
        print('***** FIND MOVIE BY TITLE *****')
        return session.query(MovieDto).filter(MovieDto.title_kor.like(title)).all()  

    @staticmethod
    def find_by_id(mov_id):
        print('***** FIND MOVIE BY ID *****')
        return session.query(MovieDto).filter(MovieDto.mov_id.like(f'{mov_id}')).one()

    @staticmethod
    def find_by_engtitle_return_id(eng_title):
        print('***** FIND MOVIE BY ENG_TITLE RETURN ID *****')
        movie = session.query(MovieDto).filter(MovieDto.title_naver_eng.like(eng_title)).one()
        movie_json = movie.json()
        mov_id = movie_json['mov_id']
        print(f'mov_id : {mov_id}')
        return mov_id

    # USE REVIEW
    @staticmethod
    def find_by_title_return_id(title):
        print('***** FIND MOVIE BY TITLE RETURN ID *****')

        movie = session.query(MovieDto).filter(MovieDto.title_kor.like(title)).one()
        print(movie)
        print(movie.json())
        movie_json = movie.json()
        mov_id = movie_json['mov_id']
        print(f'mov_id : {mov_id}')
        return mov_id

    @staticmethod
    def find_all():
        print('***** FIND ALL MOVIE *****')
        sql = session.query(MovieDto)
        df = pd.read_sql(sql.statement, sql.session.bind)
        return json.loads(df.to_json(orient='records'))

    @staticmethod
    def find_all_sort_random():
        print('***** FIND ALL MOVIE RANDOM *****')
        sql = session.query(MovieDto)
        df = pd.read_sql(sql.statement, sql.session.bind)
        df = df.sample(frac=1)  # random shuffle
        return json.loads(df.to_json(orient='records'))

    @staticmethod
    def register_movie(movie):
        print('***** NEW MOVIE DATA REGISTERING *****')
        print(movie)
        newMovie = MovieDao(mov_id = movie['mov_id'],
                            title_kor = movie['title_kor'],
                            title_naver_eng = movie['title_naver_eng'],
                            genres_kor = movie['genres_kor'],
                            keyword_kor = movie['keyword_kor'],
                            running_time_kor = movie['running_time_kor'],
                            year_kor = movie['year_kor'],
                            director_naver_kor = movie['director_naver_kor'],
                            actor_naver_kor = movie['actor_naver_kor'],
                            movie_l_rating = movie['movie_l_rating'],
                            movie_l_rating_count = movie['movie_l_rating_count'],
                            movie_l_popularity = movie['movie_l_popularity'],
                            link_naver = movie['link_naver'],
                            image_naver = movie['image_naver'])
        session.add(newMovie)
        session.commit()
        session.close()
        print('***** NEW MOVIE DATA REGISTERING COMPLETE *****')

    @staticmethod
    def modify_movie(movie):
        print('***** MOVIE DATA MODIFY *****')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
        session.query(MovieDto).filter(MovieDto.mov_id == movie['mov_id']).update({MovieDto.title_kor:movie['title_kor'],
                                                                                    MovieDto.title_naver_eng:movie['title_naver_eng'],
                                                                                    MovieDto.genres_kor:movie['genres_kor'],
                                                                                    MovieDto.keyword_kor:movie['keyword_kor'],
                                                                                    MovieDto.running_time_kor:movie['running_time_kor'],
                                                                                    MovieDto.year_kor:movie['year_kor'],
                                                                                    MovieDto.director_naver_kor:movie['director_naver_kor'],
                                                                                    MovieDto.actor_naver_kor:movie['actor_naver_kor'],
                                                                                    MovieDto.movie_l_rating:movie['movie_l_rating'],
                                                                                    MovieDto.movie_l_rating_count:movie['movie_l_rating_count'],
                                                                                    MovieDto.movie_l_popularity:movie['movie_l_popularity'],
                                                                                    MovieDto.link_naver:movie['link_naver'],
                                                                                    MovieDto.image_naver:movie['image_naver']})                                                        
        session.commit()
        session.close()
        print('***** MOVIE DATA MODIFY COMPLETE *****')

    @staticmethod
    def delete_movie(mov_id):
        print('***** MOVIE DATA DELETE *****')
        data = MovieDto.query.get(mov_id)
        db.session.delete(data)
        db.session.commit()
        db.session.close()
        print('***** MOVIE DATA DELETE COMPLETE *****')