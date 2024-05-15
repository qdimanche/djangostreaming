from django.urls import path

from . import views
from .views import MovieListView, MovieDetailView

app_name = "streaming_app"
urlpatterns = [
    path('', MovieListView.as_view(), name='index'),
    path('movie/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movie/delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
]
