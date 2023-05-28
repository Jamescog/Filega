"""
    The recommendation engine
"""

import pickle
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def recommend_movies(feature):
    with open('tfidf-model', 'rb') as file:
        tfidf = pickle.load(file)
    with open('tfidf-encoding', 'rb') as file:
        tfidf_movies = pickle.load(file)

    input_vector = tfidf.transform([feature])
    cosine_similarities = cosine_similarity(input_vector, tfidf_movies)
    
    indices = np.argsort(cosine_similarities)[0][::-1]

    top_10_movies = indices[:11]

    movie_df = pd.read_csv('cleaned_movie_data.csv')
    recommended_movies = movie_df.loc[top_10_movies, 'title']

    return recommended_movies