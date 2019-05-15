from django.urls import path
from movie.views import movie_list, movies, series, movie_detail, series_detail, download, season_detail, download_series, DownloadedToggle

urlpatterns = [
    path('', movie_list, name='home'),
    path('movies/', movies, name='movies'),
    path('movies/tag/<slug:tag_slug>/', movies, name='movies_by_slug'),
    path('series/', series, name='series'),
    path('movies/<slug:slug>/',movie_detail, name='movie_detail'),
    path('series/<slug:slug>/',series_detail, name='serie_detail'),
    path('series/<slug:slug>/<slug:season_slug>/', season_detail, name='season_detail'),
    path('series/<slug:slug>/<int:season_id>/download/<int:episode_id>', download_series, name='download_series'),
    path('movies/<slug:slug>/download/',download, name='movie_download'),

    path('saved/', DownloadedToggle.as_view(), name='saved' )
]