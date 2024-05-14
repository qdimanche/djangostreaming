import requests
import os

from django.views.generic import ListView

from streaming_app.models import Movie, Genre


def get_api_key():
    api_key_path = os.path.join(os.getcwd(), 'API_KEY')
    with open(api_key_path, 'r') as file:
        api_key = file.read().strip()
    return api_key


class MovieListView(ListView):
    template_name = 'index.html'
    context_object_name = 'movies'

    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        if search_query:
            api_key = get_api_key()
            url = f'https://www.omdbapi.com/?apikey={api_key}&t={search_query}&type=movie'
            response = requests.get(url)
            data = response.json()

            if 'Response' in data and data['Response'] == 'True':
                movie_data = data
                movie_data['omdb_id'] = movie_data['imdbID']

                movie, created = Movie.objects.get_or_create(
                    omdb_id=movie_data['omdb_id'],
                    defaults={
                        'title': movie_data.get('Title', ''),
                        'year': movie_data.get('Year', ''),
                        'poster': movie_data.get('Poster', ''),
                    }
                )

                if created:
                    genres = movie_data.get('Genre', '').split(', ')

                    for genre_name in genres:
                        genre, created = Genre.objects.get_or_create(
                            name=genre_name
                        )
                        movie.genres.add(genre)

                    movie.save()
                    print(f"Movie {movie.title} has been created.")

                return Movie.objects.filter(omdb_id=movie_data['omdb_id'])
            else:
                print("No results founded with this search arguments")
                return Movie.objects.none()
        else:
            return Movie.objects.all().order_by('-id')
