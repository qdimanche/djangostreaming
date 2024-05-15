import requests

from streaming_app.models import Movie
from streaming_app.services.genre_service import create_genre
from streaming_app.utils.api_key_utils import get_api_key
from streaming_app.utils.string_treatment_functions import remove_accents

api_key = get_api_key()


def create_movie(movie):
    try:
        movie_created, created = Movie.objects.get_or_create(
            omdb_id=movie.get('imdbID'),
            defaults={
                'title': movie.get('Title', ''),
                'year': movie.get('Year', ''),
                'poster': movie.get('Poster',
                                    'https://downtownwinnipegbiz.com/wp-content/uploads/2020/02/placeholder-image.jpg'),
                'plot': movie.get('Plot', ''),
                'director': movie.get('Director', ''),
                'metascore': movie.get('Metascore', ''),
            }
        )

        movie_created.source = 'api'
        movie_created.save()
        return movie_created
    except Movie.DoesNotExist:
        return None


def get_api_movie_details(movie_id):
    url = f'https://www.omdbapi.com/?apikey={api_key}&i={movie_id}'
    response = requests.get(url)
    return response.json()


def get_local_movies(search_query):
    """
    Perform a case-insensitive and accent-insensitive search for movies.
    """
    normalized_query = remove_accents(search_query.lower())
    movies = Movie.objects.all()
    filtered_movies = [movie for movie in movies if remove_accents(movie.title.lower()).find(normalized_query) != -1]
    return filtered_movies


def fetch_movies_from_api(search_query):
    """
    Fetch movies from the OMDB API and create them in the database.
    """
    movies_list = []
    url = f'https://www.omdbapi.com/?apikey={api_key}&s={search_query}&type=movie'
    response = requests.get(url)
    data = response.json()

    if 'Response' not in data or data['Response'] != 'True':
        print("Error while fetching movies")
        return []

    for item in data.get('Search', []):
        movie_created = create_movie(item)

        if movie_created is None:
            return

        movie_api_details = get_api_movie_details(item.get("imdbID", ""))

        genres = movie_api_details.get('Genre', '').split(', ')
        for genre_name in genres:
            genre = create_genre(genre_name)
            movie_created.genres.add(genre)

        movies_list.append(movie_created)
    return movies_list
