from django.views.generic import ListView, DetailView, View
from django.shortcuts import redirect
from .models import Movie
from django.http import HttpResponseNotAllowed
from .services.movie_service import get_local_movies, fetch_movies_from_api


class DeleteMovieView(View):
    http_method_names = ['post']

    def post(self, request, movie_id):
        try:
            movie = Movie.objects.get(id=movie_id)
            movie.delete()
        except Movie.DoesNotExist:
            return HttpResponseNotAllowed(['POST'])
        return redirect('streaming_app:index')


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

        return fetch_movies_from_api(search_query)


class MovieDetailView(DetailView):
    model = Movie
    template_name = 'movie_detail.html'
    context_object_name = 'movie'
