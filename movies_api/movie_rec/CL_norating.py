#Referece:https://medium.com/analytics-vidhya/implementation-of-a-movies-recommender-from-implicit-feedback-6a810de173ac

import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix, save_npz, load_npz, vstack, hstack, lil_matrix
import implicit
import pickle
from implicit.evaluation import train_test_split, precision_at_k, mean_average_precision_at_k
from .importdata import collabFilter

import os

PATH =os.path.dirname(os.path.realpath(__file__))

class CL2(object):
    def __init__(self,CF=collabFilter(),):
        self.CF=CF
        #self.movies,self.ratings = CF.loadData_f()
        #exit()


    def load_data(self):

        self.movies,self.ratings = self.CF.loadData_f()

        return self.ratings, self.movies

    def sparse_matrices(self,df):


    # using a scalar value (40) to convert ratings from a scale (1-5) to a like/click/view (1)
        alpha = 40
        #alpha = df['rating'].apply(pd.to_numeric)
        sparse_user_item = csr_matrix(([alpha]*len(df['movieId']), (df['userId'], df['movieId'])))

        # transposing the item-user matrix to create a user-item matrix
        sparse_item_user = sparse_user_item.T.tocsr()
        # save the matrices for recalculating user on the fly
        save_npz("sparse_user_item_NR.npz", sparse_user_item)
        save_npz("sparse_item_user_NR.npz", sparse_item_user)

        return sparse_user_item, sparse_item_user

    def most_similar_items(self,item_id, n_similar=10):

        with open('model_NR.sav', 'rb') as pickle_in:
            model = pickle.load(pickle_in)

        similar, _ = zip(*model.similar_items(item_id, n_similar)[1:])
        return similar


    def model(self):

        sparse_item_user = load_npz("sparse_item_user_NR.npz")

        train, test = train_test_split(sparse_item_user, train_percentage=0.8)

        model = implicit.als.AlternatingLeastSquares(factors=100,
            regularization=0.1, iterations=20, calculate_training_loss=False)
        model.fit(train)

        with open('model_NR.sav', 'wb') as pickle_out:
            pickle.dump(model, pickle_out)

    def evaloutput(self,K=10):
        with open('model_NR.sav', 'rb') as pickle_in:
            model = pickle.load(pickle_in)
        sparse_item_user = load_npz("sparse_user_item_NR.npz")
        train, test = train_test_split(sparse_item_user, train_percentage=0.8)
        #p_at_k = precision_at_k(model, K, train_user_items=train, test_user_items=test)
        print("test",test.shape)
        print("train",train.shape)
        p_at_k = precision_at_k(model, train, test, K)
        m_at_k = mean_average_precision_at_k(model, train, test, K)

        return p_at_k, m_at_k


    def recalculate_user(self,selectmovie_id,user_ratings):

        m = load_npz(PATH+'/sparse_user_item_NR.npz')
        n_users, n_movies = m.shape
        ratings = user_ratings
        id = selectmovie_id
        #ratings = [user_ratings for i in range(len(user_ratings))]
        #id = [selectmovie_id for i in range(len(user_ratings))]
        m.data = np.hstack((m.data, ratings))

        m.indices = np.hstack((m.indices, id))
        m.indptr = np.hstack((m.indptr, len(m.data)))
        m._shape = (n_users + 1, n_movies)

        # recommend N items to new user
        with open(PATH+'/model_NR.sav', 'rb') as pickle_in:
            model = pickle.load(pickle_in)
        recommended, _ = zip(*model.recommend(n_users, m, recalculate_user=True))

        #return recommended, self.map_movies(recommended)

        return recommended

#CF2=CL2()
#ratings,movies = CF2.load_data()

#sparse_user_item, sparse_item_user = CF2.sparse_matrices(ratings)
#CF2.model()
#print(sparse_item_user)
#p_at_k, m_at_k = model()
#CF2.model()
#result=CF2.recalculate_user([2],[3])
#print(result)
#a = load_npz('sparse_user_item.npz')
#print("sparse_user:\n"+str(a))
#print(map_movies([2,3,4]))

#print(p_at_k, m_at_k)