import pandas as pd
import ast
import nltk
import re
import csv

# Load the movie data into a DataFrame
movie_df = pd.read_csv('movie_data.csv')

# Drop rows with missing values in any column
movie_df.dropna(axis=0, how='any', inplace=True)

# Initialize the vocabulary
vocabulary = nltk.FreqDist()

# Iterate over each movie summary
for summary in movie_df['summary']:
    # Split the summary into individual words
    words = summary.split()
    # Update the vocabulary with the words
    vocabulary.update(words)

# Get the most frequent 200 words
most_common_words = vocabulary.most_common(200)

# Extract the most common words
most_common_list = [word for word, count in most_common_words]

# Perform cleaning on summaries and create 'clean_summary' column
lemmatizer = nltk.stem.WordNetLemmatizer()
clean_freq = [lemmatizer.lemmatize(word) for word in most_common_list]
clean_summaries = []
for summary in movie_df['summary']:
    features = re.split(' |-', summary)
    features = [word for word in features if word.isalpha()]
    features = [word.lower() for word in features]
    features = [lemmatizer.lemmatize(word) for word in features]
    features = [word for word in features if word not in clean_freq]

    if features:
        clean_summaries.append(" ".join(features))
    else:
        clean_summaries.append('')

# Assign 'clean_summary' column to the DataFrame
movie_df['clean_summary'] = clean_summaries

# Create the 'feature' column
combined_strings = []
for index, row in movie_df.iterrows():
    genre = ast.literal_eval(row['genre'])
    actors = ast.literal_eval(row['actors'])
    director = ast.literal_eval(row['directors'])
    actors = [a.replace("'", "*") for a in actors]
    director = [d.replace("'", "*") for d in director]
    summary = row['clean_summary']

    # Format genre, actors, and director
    genre_str = ' '.join([f"genre-{g.lower()}" for g in genre])
    actors_str = ' '.join([f"actor-{a.lower().replace(' ', '+')}" for a in actors])
    director_str = ' '.join([f"director-{d.replace(' ', '+')}" for d in director])
    

    # Create the combined string
    combined_string = f"{genre_str} {actors_str} {director_str} Summary: {summary}"
    combined_strings.append(combined_string)

# Assign 'feature' column to the DataFrame
movie_df['feature'] = combined_strings

# Save the modified DataFrame to a new CSV file
movie_df.to_csv('cleaned_movie_data.csv', index=False, quoting=csv.QUOTE_NONNUMERIC)
# Print the DataFrame with the 'feature' column
print(movie_df['feature'])
