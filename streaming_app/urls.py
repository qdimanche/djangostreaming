from django.urls import path
from .views import MovieListView

app_name = "streaming_app"
urlpatterns = [
    path('', MovieListView.as_view(), name='index'),
]
