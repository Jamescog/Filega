from flask import Flask, render_template, request
from flask_cors import CORS
import json
import pandas as pd
from the_engine import recommend_movies

df = pd.read_csv('cleaned_movie_data.csv')
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    with open('movie_titles.json') as f:
        movie_titles = json.load(f)
    return render_template('index.html', movie_titles=movie_titles)

@app.route('/recommend', methods=['GET'])
def recommend():
    name = request.args.get('name')
    movie = df[df['title'] == name].iloc[0]
    title = movie['title']
    genre = movie['genre'].strip("[]'")
    actors = [actor.strip("[]'") for actor in movie['actors'].split(', ')]
    actors = actors[:5]
    director = movie['directors'][0].strip("[]'")
    recommended_movies = recommend_movies(movie['feature'])
    recommended_movies = recommended_movies[1:]

    recommended_movies_info = []
    for recommended_movie in recommended_movies:
        recommended_movie_info = df[df['title'] == recommended_movie].iloc[0]
        recommended_movie_title = recommended_movie_info['title']
        recommended_movie_genre = recommended_movie_info['genre'].strip("[]'")
        recommended_movie_actors = [actor.strip("[]'") for actor in recommended_movie_info['actors'].split(', ')]
        recommended_movie_actors = recommended_movie_actors[:5]
        recommended_movie_director = recommended_movie_info['directors'].strip("[]'")

        recommended_movie_dict = {
            'title': recommended_movie_title,
            'genre': recommended_movie_genre,
            'actors': recommended_movie_actors,
            'directors': recommended_movie_director
        }
        recommended_movies_info.append(recommended_movie_dict)
    
    movie_info = {
        'title': title,
        'genre': genre,
        'actors': actors,
        'directors': director
    }
    
    return render_template('recommendations.html', recommended_movies=recommended_movies_info, movie_info=movie_info)


if __name__ == '__main__':
    app.run()
