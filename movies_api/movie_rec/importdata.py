#Reference: https://github.com/CaseyAMeakin/MovieTime/blob/master/batch/collabFilter.py#L78
#Reference: https://medium.com/analytics-vidhya/implementation-of-a-movies-recommender-from-implicit-feedback-6a810de173ac
import pandas as pd
#import requests
#import json
import MySQLdb
from pandas import DataFrame
from numpy import *
import numpy as np
from sklearn.model_selection import train_test_split
import random
from scipy.sparse import csr_matrix, save_npz, load_npz, vstack, hstack, lil_matrix
#import implicit
import pickle
#from implicit.evaluation import train_test_split, precision_at_k, mean_average_precision_at_k


class collabFilter(object):
    def __init__(self,host='localhost',db='ratings',dbuser='root',dbpw='7878158'):
        self.host =host
        self.db = db
        self.dbuser = dbuser
        self.dbpw = dbpw
        self.con = None
        self.cur = None

        self.ratings = []
        self.movies = []

    def getCursor(self):
        if not self.cur:
            try:
                self.con = MySQLdb.connect(host=self.host,db=self.db, user=self.dbuser, passwd=self.dbpw)
                self.cur = self.con.cursor()
            except:
                print
                'Trouble connecting to MySQL db'
                self.con = None
                self.cur = None


#db=MySQLdb.connect(host="localhost",
                   #user="root",
                   #passwd="7878158",
                   #db="ratings")
    # cur = db.cursor()

    # cur.execute("Select * FROM movies LIMIT 100")
    # for row in cur.fetchall():
    # print(row)

    def trySqlFetchall(self, sqlcmd):
        if not self.cur: self.getCursor()
        if not self.cur: return None
        try:
            curcall = self.cur.execute(sqlcmd)
            query = self.cur.fetchall()
        except:
            query = None
        return query

    def loadData(self):
        query1 = self.trySqlFetchall('Select movies.movieId,movies.title FROM movies')
        query2 = self.trySqlFetchall('Select movie_ratings.userId,movie_ratings.movieId,movie_ratings.rating FROM movie_ratings')
        #print(str(query1))
        movies = pd.DataFrame(list(query1), columns =['movieId','title'])
        #movies = movies.to_numpy()
        ratings = DataFrame(list(query2),columns = ['userId','movieId','rating'])
        #ratings =ratings.to_numpy(dtype=np.int)
        with open("movies.pkl",'wb') as fout:
            pickle.dump(movies,fout)
        with open("ratings.pkl",'wb') as fout:
            pickle.dump(ratings,fout)
        return movies,ratings

    def loadData_f(self):
        with open("movies.pkl",'rb') as fout:
            movies = pickle.load(fout)
        with open("ratings.pkl",'rb') as fout:
            ratings = pickle.load(fout)
        return movies,ratings



#CF = collabFilter()
#movies,ratings = CF.loadData_f()
#print(movies)
#print(ratings['rating'].apply(pd.to_numeric))
#print(type(ratings.values[:,2]))
#train, test = train_test_split(ratings, test_size=0.2)
#print('Train:',train)
#movieid = []
#title = []

#for item in moviedata:
    #movieid = item['movieid']
    #movieid.append(movieid)
    #title = item['title']
    #title.append(title)
#print("movieid",movieid)


#alluserid = []
#all_sep_rating = []

#for id in len(movieid):
    #ratingapi = requests.get("http://99.79.10.143:3300/api/rating/1?detail=" + id)
    #rating = ratingapi.json()
    #rating =rating[data]

    #for item in rating:
        #userid = item["userid"]
        #alluserid.append(userid)
        #sep_rating = item["rating"]
        #all_sep_rating = sep_rating.append(rating)
#print('alluserid',userid)
#print('all_sep_rating',rating)

#ratings = pd.DataFrame()

#ratings = pd.read_csv('ratings.csv')
#movies = pd.read_csv('movies.csv')
#ratings = pd.merge(movies,ratings).drop(['genres','timestamp'],axis=1)
#ratings = ratings.head(2400000)
#print(ratings.shape)
#print("ratings",ratings)

#userRatings = pd.pivot(ratings, index='userId',columns='title',values='rating')
#print("userRatings",userRatings)
#userRatings.head()
#print("Before: ",userRatings.shape)
#userRatings = userRatings.dropna(thresh=10, axis=1).fillna(0,axis=1)
#userRatings.fillna(0, inplace=True)
#print("After: ",userRatings.shape)


#corrMatrix = userRatings.corr(method='pearson')

#def get_similar(movie_name,rating):
    #similar_ratings = corrMatrix[movie_name]*(rating-2.5)
    #similar_ratings = similar_ratings.sort_values(ascending=False)
    #print(type(similar_ratings))
    #return similar_ratings

#romantic_lover = [("Toy Story (1995)",5),("Jumanji (1995)",3),("Screamers (1995)",1)]
#similar_movies = pd.DataFrame()

#for movie,rating in romantic_lover:
    #similar_movies = similar_movies.append(get_similar(movie,rating),ignore_index = True)


#for movie, rating in romantic_lover:
    #del similar_movies[movie]


#print("simliar movies matrix",similar_movies)
#print("similar movies:",similar_movies.sum().sort_values(ascending=False).head(5))

