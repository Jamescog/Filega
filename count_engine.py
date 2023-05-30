import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def recommend_movies(feature):
    with open('count-model', 'rb') as file:
        count_vect = pickle.load(file)
    with open('count-encoding', 'rb') as file:
        count_movies = pickle.load(file)

    input_vector = count_vect.transform([feature])
    cosine_similarities = cosine_similarity(input_vector, count_movies)
    
    indices = np.argsort(cosine_similarities)[0][::-1]

    top_10_movies = indices[:10]

    movie_df = pd.read_csv('cleaned_movie_data.csv')
    recommended_movies = movie_df.loc[top_10_movies, 'title']

    return recommended_movies