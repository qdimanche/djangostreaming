import requests

from streaming_app.models import Movie, Genre


def get_local_movies(search_query):
    return Movie.objects.filter(title__icontains=search_query)


def fetch_movies_from_api(api_key, search_query):
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
