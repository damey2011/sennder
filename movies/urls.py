from django.urls import path

from movies import views

app_name = 'movies'

urlpatterns = [
    path('', views.MoviesListView.as_view(), name='list')
]
