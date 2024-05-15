from django.views.generic import ListView, DetailView
from django.shortcuts import redirect
from .models import Movie
from django.http import HttpResponseNotAllowed
from .services.movie_service import get_local_movies, fetch_movies_from_api
from .utils.api_key_utils import get_api_key


def delete_movie(request, movie_id):
    if request.method == 'POST':
        try:
            movie = Movie.objects.get(id=movie_id)
            movie.delete()
        except Movie.DoesNotExist:
            return HttpResponseNotAllowed(['POST'])
        return redirect('streaming_app:index')
    else:
        return HttpResponseNotAllowed(['POST'])


class MovieListView(ListView):
    template_name = 'index.html'
    context_object_name = 'movies'

    def get_queryset(self):
        search_query = self.request.GET.get('search_query')
        if not search_query:
            movies = Movie.objects.all().order_by('-id')
            for movie in movies:
                movie.source = "database"
            return movies

        local_movies = get_local_movies(search_query)
        if local_movies:
            for movie in local_movies:
                movie.source = "database"
            return local_movies

        api_key = get_api_key()
        return fetch_movies_from_api(api_key, search_query)


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'
    context_object_name = 'movie'
