import timeit

import requests
from django.core.cache import caches
from django.test import TestCase
from django.urls import reverse

from movies.api_service import GhibliAPI, GhibliAPIException
from movies.views import MoviesListView


class GhibliMoviesTest(TestCase):
    def setUp(self) -> None:
        self.default_cache = caches['default']

    def clear_movies_cache(self) -> None:
        if MoviesListView.cache_key in self.default_cache:
            self.default_cache.delete(MoviesListView.cache_key)

    def test_movie_page_url_resolves_correctly(self) -> None:
        self.assertEqual(reverse('movies:list'), '/movies/')

    def test_that_movies_page_is_accessible(self) -> None:
        response = self.client.get(reverse('movies:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_that_ghibli_api_is_available(self) -> None:
        response = requests.get(GhibliAPI.BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_that_invalid_endpoint_raises_exception(self) -> None:
        with self.assertRaises(GhibliAPIException):
            GhibliAPI.get(f'{GhibliAPI.BASE_URL}/fkdnfif')

    def test_that_ghibli_people_function_returns_valid_data(self) -> None:
        people = GhibliAPI._list_people()
        self.assertIsInstance(people, list)
        if len(people):
            self.assertIsNotNone(people[0].get('id'))

    def test_that_ghibli_movies_function_returns_valid_data(self) -> None:
        movies = GhibliAPI._list_movies()
        self.assertIsInstance(movies, list)
        if len(movies):
            self.assertIsNotNone(movies[0].get('id'))

    def test_that_api_response_is_correctly_passed_to_template_context(self) -> None:
        movies = GhibliAPI.get_movies_and_their_actors()
        response = self.client.get(reverse('movies:list'))
        self.assertEqual(movies, response.context['movies'])

    def test_that_page_was_cached_between_requests(self) -> None:
        self.clear_movies_cache()
        execution_time_before_cache = timeit.timeit(
            lambda: self.client.get(reverse('movies:list')), number=1
        )
        execution_time_after_cache = timeit.timeit(
            lambda: self.client.get(reverse('movies:list')), number=1
        )
        self.assertEqual(MoviesListView.cache_key in self.default_cache, True)
        self.assertGreater(execution_time_before_cache, execution_time_after_cache)

    def tearDown(self) -> None:
        self.clear_movies_cache()
