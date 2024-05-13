from django.urls import path
from .views import MovieListView, AddMovieView

app_name = "streaming_app"
urlpatterns = [
    path('', MovieListView.as_view(), name='index'),
    path('add_movie/', AddMovieView.as_view(), name='add_movie'),
]
