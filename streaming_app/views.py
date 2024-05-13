import requests
import os

from django.views.generic import ListView

from streaming_app.models import Movie


def get_api_key():
    api_key_path = os.path.join(os.getcwd(), 'API_KEY')
    with open(api_key_path, 'r') as file:
        api_key = file.read().strip()
    return api_key


class MovieListView(ListView):
    template_name = 'index.html'
    context_object_name = 'movies'

    def get_queryset(self):
        return Movie.objects.all()


class AddMovieView(ListView):
    template_name = 'add_movie.html'
    context_object_name = 'movies'

    def get_queryset(self):
        api_key = get_api_key()
        search_query = 'Harry'
        url = f'https://www.omdbapi.com/?apikey={api_key}&s={search_query}'
        response = requests.get(url)
        data = response.json()
        return data.get('Search', [])
