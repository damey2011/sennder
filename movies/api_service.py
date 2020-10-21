import re
import requests
from collections import defaultdict


class GhibliAPIException(BaseException):
    pass


class GhibliAPI:
    BASE_URL = 'https://ghibliapi.herokuapp.com'
    FILM_ID_REGEX = re.compile(r'https?://[\w+.]*/films/([\w+\-]*)')

    @classmethod
    def get_film_id_from_url(cls, url: str) -> str:
        return re.findall(cls.FILM_ID_REGEX, url)[0]

    @classmethod
    def get(cls, endpoint: str):
        response = requests.get(endpoint)
        if response.status_code == 200:
            return response.json()
        raise GhibliAPIException(f'Request to {endpoint} returned with status code {response.status_code}')

    @classmethod
    def _list_movies(cls) -> list:
        return cls.get(f'{cls.BASE_URL}/films')

    @classmethod
    def _list_people(cls) -> list:
        return cls.get(f'{cls.BASE_URL}/people')

    @classmethod
    def get_movies_and_their_actors(cls) -> list:
        movies = cls._list_movies()
        people = cls._list_people()
        movies_to_people = defaultdict(lambda: list())
        for person in people:
            for movie in person.get('films'):
                if isinstance(person, dict):
                    movies_to_people[cls.get_film_id_from_url(movie)].append(person)
        for movie in movies:
            people = movies_to_people.get(movie.get('id'), list())
            movie['people'] = people
        return movies
