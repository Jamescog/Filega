"""
    Train the model and encode it
"""

import pandas as pd
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv('cleaned_movie_data.csv')
df['feature'] = df.feature.values.astype('U')
tfidf = TfidfVectorizer()
tfidf.fit(df['feature'])
tfidf_movies = tfidf.transform(df['feature'])

with open('tdidf-model', 'wb') as file:
    pickle.dump(tfidf, file)

with open('tfidf-encoding', 'wb') as file:
    pickle.dump(tfidf_movies, file)