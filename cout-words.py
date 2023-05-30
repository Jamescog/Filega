import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv('cleaned_movie_data.csv')
df['feature'] = df.feature.values.astype('U')
count_vect = CountVectorizer()
count_vect.fit(df['feature'])
count_movies = count_vect.transform(df['feature'])

with open('count-model', 'wb') as file:
    pickle.dump(count_vect, file)

with open('count-encoding', 'wb') as file:
    pickle.dump(count_movies, file)