import requests
import unicodedata
from streaming_app.models import Movie, Genre


def remove_accents(input_str):
    """
    Normalize strings to remove accents and perform a case-insensitive comparison.
    """
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)])


def get_local_movies(search_query):
    """
    Perform a case-insensitive and accent-insensitive search for movies.
    """
    normalized_query = remove_accents(search_query.lower())
    movies = Movie.objects.all()
    filtered_movies = [movie for movie in movies if remove_accents(movie.title.lower()).find(normalized_query) != -1]
    return filtered_movies


def fetch_movies_from_api(api_key, search_query):
    """
    Fetch movies from the OMDB API and create them in the database.
    """
    movies_list = []
    url = f'https://www.omdbapi.com/?apikey={api_key}&s={search_query}&type=movie'
    response = requests.get(url)
    data = response.json()

    if 'Response' not in data or data['Response'] != 'True':
        return print("Error while fetching movies")

    for item in data.get('Search', []):
        movie, created = Movie.objects.get_or_create(
            omdb_id=item.get('imdbID'),
            defaults={
                'title': item.get('Title', ''),
                'year': item.get('Year', ''),
                'poster': item.get('Poster',
                                   'https://downtownwinnipegbiz.com/wp-content/uploads/2020/02'
                                   '/placeholder-image.jpg'),
                'plot': item.get('Plot', ''),
                'director': item.get('Director', ''),
                'metascore': item.get('Metascore', ''),
            }
        )

        if not created:
            return print('Error while adding movie')

        movie.source = 'api'
        movie.save()

        genres = item.get('Genre', '').split(', ')
        for genre_name in genres:
            genre, created = Genre.objects.get_or_create(name=genre_name.strip())

            if not created:
                print('Error while adding genres')

            movie.genres.add(genre)

        movies_list.append(movie)
    return movies_list
