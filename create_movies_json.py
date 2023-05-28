import csv
import json

csv_file = 'cleaned_movie_data.csv'
json_file = 'movie_titles.json'

# Read the CSV file and extract the movie titles
movie_titles = []
with open(csv_file, 'r', newline='') as file:
    reader = csv.DictReader(file)
    for row in reader:
        movie_titles.append(row['title'])

# Write the movie titles to a JSON file
with open(json_file, 'w') as file:
    json.dump(movie_titles, file)

print("JSON file created successfully!")
