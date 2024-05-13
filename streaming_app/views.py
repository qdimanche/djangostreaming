import requests
import os

from django.shortcuts import redirect
from django.views import View
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
        return Movie.objects.all().order_by('-id')


class AddMovieView(ListView):
    template_name = 'add_movie.html'
    context_object_name = 'movies'

    def get_queryset(self):
        api_key = get_api_key()
        search_query = self.request.GET.get('search_query')
        if not search_query:
            raise ValueError("A search query is required.")
        url = f'https://www.omdbapi.com/?apikey={api_key}&s={search_query}'
        response = requests.get(url)
        data = response.json()

        # Ajouter l'ID unique fourni par l'API OMDB à chaque film
        for i, movie_data in enumerate(data.get('Search', [])):
            movie_data['omdb_id'] = movie_data['imdbID']

        return data.get('Search', [])


class AddToLibraryView(View):
    def get(self, request, *args, **kwargs):
        api_key = get_api_key()
        omdb_id = kwargs['movie_id']
        url = f'https://www.omdbapi.com/?apikey={api_key}&i={omdb_id}'
        response = requests.get(url)
        movie_data = response.json()

        movie, created = Movie.objects.get_or_create(
            omdb_id=omdb_id,
            defaults={
                'title': movie_data['Title'],
                'year': movie_data['Year'],
                'type': movie_data['Type'],
                'poster': movie_data['Poster']
            }
        )

        if created:
            movie.save()

        return redirect('streaming_app:index')
