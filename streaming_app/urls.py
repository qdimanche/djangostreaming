from django.urls import path
from .views import MovieListView, AddMovieView, AddToLibraryView

app_name = "streaming_app"
urlpatterns = [
    path('', MovieListView.as_view(), name='index'),
    path('add_movie/', AddMovieView.as_view(), name='add_movie'),
    path('add_to_library/<str:movie_id>/', AddToLibraryView.as_view(), name='add_to_library'),
]
