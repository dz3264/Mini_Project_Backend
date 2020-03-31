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
        #alpha = 40
        alpha = df['rating'].apply(pd.to_numeric)
        sparse_user_item = csr_matrix((alpha, (df['userId'], df['movieId'])))
        #sparse_user_item = csr_matrix( ([alpha]*len(df['movie_id']), (df['user_id'], df['movie_id']) ))
        # transposing the item-user matrix to create a user-item matrix
        sparse_item_user = sparse_user_item.T.tocsr()
        # save the matrices for recalculating user on the fly
        save_npz("sparse_user_item2.npz", sparse_user_item)
        save_npz("sparse_item_user2.npz", sparse_item_user)

        return sparse_user_item, sparse_item_user

    def map_movies(self,movie_ids):

        #df = movies
        df = pd.read_csv('ml-1m/movies.dat', delimiter='::', header=None,
                     names=['movie_id', 'title', 'genre'], engine='python')

     # add years to a new column 'year' and remove them from the movie title
        df['year'] = df['title'].str[-5:-1]
        df['title'] = df['title'].str[:-6]

    # creates an ordered list of dictionaries with the movie information for all movie_ids
        #mapped_movies = [df[df['movieId'] == i].to_dict('records')[0] for i in movie_ids]
        mapped_movies = [df[df['movie_id'] == i].to_dict('records')[0] for i in movie_ids]
        return mapped_movies

    def map_users(self,user_ids):

        df = pd.read_csv('ml-1m/users.dat', delimiter='::', header=None,
                     names=['user_id', 'gender', 'agerange', 'occupation', 'timestamp'], engine='python')
        df = df.drop(['timestamp'], axis=1)

        mapped_users = [df[df['user_id'] == i].to_dict('records')[0] for i in user_ids]

        return mapped_users

    def most_similar_items(self,item_id, n_similar=10):

        with open('model2.sav', 'rb') as pickle_in:
            model = pickle.load(pickle_in)

        similar, _ = zip(*model.similar_items(item_id, n_similar)[1:])
        return similar
        #return self.map_movies(similar)


    def most_similar_users(self,user_id, n_similar=10):

        sparse_user_item = load_npz("sparse_user_item2.npz")

        with open('model2.sav', 'rb') as pickle_in:
         model = pickle.load(pickle_in)

        # similar users gives back [(users, scores)]
        # we want just the users and not the first one, because that is the same as the original user
        similar, _ = zip(*model.similar_users(user_id, n_similar)[1:])

        # orginal users items
        original_user_items = list(sparse_user_item[user_id].indices)

        # # this maps back user_ids to their information, which is useful for visualisation
        similar_users_info = map_users(similar)
        # # now we want to add the items that a similar used has rated
        for user_info in mapped:
        # we create a list of items that correspond to the simillar user ids
        # then compare that in a set operation to the original user items
        # as a last step we add it as a key to the user information dictionary
            user_info['items'] = set(list(sparse_user_item[user_info['user_id']].indices)) & set(original_user_items)

        return similar_users_info

    def model(self):

        sparse_item_user = load_npz("sparse_item_user2.npz")

        train, test = train_test_split(sparse_item_user, train_percentage=0.8)

        model = implicit.als.AlternatingLeastSquares(factors=100,
            regularization=0.1, iterations=20, calculate_training_loss=False)
        model.fit(train)

        with open('model2.sav', 'wb') as pickle_out:
            pickle.dump(model, pickle_out)

    def evaloutput(self,K=10):
        with open('model2.sav', 'rb') as pickle_in:
            model = pickle.load(pickle_in)
        sparse_item_user = load_npz("sparse_user_item2.npz")
        train, test = train_test_split(sparse_item_user, train_percentage=0.8)
        #p_at_k = precision_at_k(model, K, train_user_items=train, test_user_items=test)
        print("test",test.shape)
        print("train",train.shape)
        p_at_k = precision_at_k(model, train, test, K)
        m_at_k = mean_average_precision_at_k(model, train, test, K)

        return p_at_k, m_at_k

    def recommend(self,user_id):

        sparse_user_item = load_npz("sparse_user_item2.npz")

        with open('model2.sav', 'rb') as pickle_in:
            model = pickle.load(pickle_in)

        recommended, _ =  zip(*model.recommend(user_id, sparse_user_item))

        return recommended, self.map_movies(recommended)

    def recommend_all_users(self):

        sparse_user_item = load_npz("sparse_user_item2.npz")

        with open('model2.sav', 'rb') as pickle_in:
            model = pickle.load(pickle_in)

         # numpy array with N recommendations for each user
        # remove first array, because those are the columns
        all_recommended = model.recommend_all(user_items=sparse_user_item, N=10,
        recalculate_user=False, filter_already_liked_items=True)[1:]

    # create a new Pandas Dataframe with user_id, 10 recommendations, for all users
        df = pd.read_csv('ml-1m/users.dat', delimiter='::', header=None, names=['user_id', 'gender', 'agerange', 'occupation', 'timestamp'], engine='python')
        df = df.drop(['gender', 'agerange', 'occupation', 'timestamp'], axis=1)
        df[['rec1', 'rec2', 'rec3', 'rec4', 'rec5', 'rec6', 'rec7', 'rec8', 'rec9', 'rec10']] = pd.DataFrame(all_recommended)
        df.to_pickle("all_recommended.pkl")
        return df


    def recalculate_user(self,selectmovie_id,user_ratings):

        m = load_npz(PATH+'/sparse_user_item2.npz')
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
        with open(PATH+'/model2.sav', 'rb') as pickle_in:
            model = pickle.load(pickle_in)
        recommended, _ = zip(*model.recommend(n_users, m, recalculate_user=True))

        #return recommended, self.map_movies(recommended)

        return recommended

#CF2=CL2()
#ratings,movies = CF2.load_data()

#sparse_user_item, sparse_item_user = CF2.sparse_matrices(ratings)
#print(sparse_item_user)
#p_at_k, m_at_k = model()
#CF2.model()
#result=CF2.recalculate_user([2],[3])
#print(result)
#a = load_npz('sparse_user_item.npz')
#print("sparse_user:\n"+str(a))
#print(map_movies([2,3,4]))
#print(a.indptr)
#print(p_at_k, m_at_k)