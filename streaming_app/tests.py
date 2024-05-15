from django.test import TestCase, RequestFactory
from django.urls import reverse
from .models import Movie
from .views import DeleteMovieView, MovieListView, MovieDetailView


class DeleteMovieViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.movie = Movie.objects.create(title='Test Movie')

    def test_post_delete_movie(self):
        request = self.factory.post(reverse('streaming_app:delete_movie', kwargs={'movie_id': self.movie.id}))
        response = DeleteMovieView.as_view()(request, movie_id=self.movie.id)
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertFalse(Movie.objects.filter(id=self.movie.id).exists())


class CreateMovieViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.movie = Movie.objects.create(title='Test Movie')


class MovieListViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.movie = Movie.objects.create(title='Test Movie')

    def test_get_queryset(self):
        request = self.factory.get('/?search_query=')
        response = MovieListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.movie, response.context_data['movies'])


class MovieDetailViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.movie = Movie.objects.create(title='Test Movie')

    def test_get_movie_detail(self):
        request = self.factory.get(reverse('streaming_app:movie_detail', kwargs={'pk': self.movie.pk}))
        response = MovieDetailView.as_view()(request, pk=self.movie.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data['movie'], self.movie)
