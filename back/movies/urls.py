from django.urls import path
from . import views
from .views import FetchMoviesAPIView, FetchGenresAPIView

urlpatterns = [
    path('movies/', views.movie_list),
    path('movies/genres/', views.genre_list),
    # path('movies/<int:movie_pk>/similar/', views.similar_movies),
    path('movies/<int:movie_pk>/', views.movie_detail),
    path('movies/<int:movie_pk>/<int:user_pk>/', views.read_lhf),
    path('fetch-movies/', FetchMoviesAPIView.as_view(), name='fetch-movies'),
    path('get-genres/', FetchGenresAPIView.as_view(), name='get-genres'),
    path("filter-genre/<int:genre_pk>/", views.filter_genre, name="filter_genre"),

    path("movies/<int:movie_pk>/likes/<int:user_pk>/", views.movie_likes, name="movie_likes"),
    path("movies/liked_genres/<int:user_pk>/", views.liked_genres_with_movies, name="liked_genres_with_movies"),
    path("movies/<int:movie_pk>/hates/<int:user_pk>/", views.movie_hates, name="movie_hates"),
    path("movies/<int:movie_pk>/favorite/<int:user_pk>/", views.movie_favorite, name="movie_favorite"),
    path('movies/recommend/weekday/', views.today_recommend),
    path('movies/recommend/korea/', views.korean_movies),
    path('movies/recommend/week/', views.week_recommend),
    path('movies/<int:user_pk>/profile_favorite/', views.profile_favorite),
    path('movies/<int:user_pk>/profile_like/', views.profile_like),
    path('movies/<int:user_pk>/my_favorite/', views.my_favorite),
    path('search/', views.search),
    path('movies/<int:movie_pk>/related/', views.related_movies, name='related-movies'),
    path('movies/<int:user_pk>/user_recommend/', views.user_recommend),
]



