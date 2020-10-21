from django.core.cache import caches
from django.views.generic import TemplateView

from movies.api_service import GhibliAPI


class MoviesListView(TemplateView):
    template_name = 'index.html'
    cache_key = 'movie_list'
    cache_expiry = 300

    def get_context_data(self, **kwargs):
        ctx = super(MoviesListView, self).get_context_data(**kwargs)
        default_cache = caches['default']
        movies = ctx['movies'] = default_cache.get(self.cache_key)
        if not movies:
            movies = ctx['movies'] = GhibliAPI.get_movies_and_their_actors()
            default_cache.set(self.cache_key, movies, self.cache_expiry)
        return ctx
