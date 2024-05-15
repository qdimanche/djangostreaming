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
    url = f'https://www.omdbapi.com/?apikey={api_key}&s={search_query}&type=movie'
    response = requests.get(url)
    data = response.json()

    if 'Response' in data and data['Response'] == 'True':
        movies_list = []
        for item in data.get('Search', []):
            imdb_id = item.get('imdbID')
            movie, created = Movie.objects.get_or_create(
                omdb_id=imdb_id,
                defaults={
                    'title': item.get('Title', ''),
                    'year': item.get('Year', ''),
                    'poster': item.get('Poster',
                                       'https://downtownwinnipegbiz.com/wp-content/uploads/2020/02'
                                       '/placeholder-image.jpg'),
                }
            )

            if created:
                detail_url = f'https://www.omdbapi.com/?apikey={api_key}&i={imdb_id}'
                detail_response = requests.get(detail_url)
                detail_data = detail_response.json()

                movie.plot = detail_data.get('Plot', '')
                movie.director = detail_data.get('Director', '')
                movie.metascore = detail_data.get('Metascore', '')

                genres = detail_data.get('Genre', '').split(', ')
                for genre_name in genres:
                    genre, _ = Genre.objects.get_or_create(name=genre_name.strip())
                    movie.genres.add(genre)

                movie.save()
                movie.source = "api"
                print(f"Movie {movie.title} has been created.")
            movies_list.append(movie)
        return movies_list
    else:
        print("No results found with this search arguments")
        return []
