from django.urls import path
from .views import MovieListView, MovieDetailView, DeleteMovieView

app_name = "streaming_app"
urlpatterns = [
    path('', MovieListView.as_view(), name='index'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movie/delete/<int:movie_id>/', DeleteMovieView.as_view(), name='delete_movie'),
]
