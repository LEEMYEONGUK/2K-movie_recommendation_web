from rest_framework import serializers
from .models import Movie, Genre
from accounts.models import User


class GenreMoviesSerializer(serializers.Serializer):
    class MovieListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = ('pk', 'title', 'overview','release_date','poster_path','vote_count','vote_average', 'backdrop_path')
            
    genre = serializers.CharField(source='genre.name')
    movies = MovieListSerializer(many=True)

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'


class GenreListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

class MovieListSerializer(serializers.ModelSerializer):
    class UserInfoSerializer(serializers.ModelSerializer):
        class Meta:
            model=User
            fields=('username',)
    user=UserInfoSerializer(read_only=True)
    class Meta:
        model = Movie
        fields = ('pk', 'title', 'overview','release_date','poster_path','vote_count','vote_average', 'backdrop_path', 'user')



class MovieReadSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = ('tmdb_id', 'title', 'overview','release_date','poster_path','vote_count','vote_average','backdrop_path', 'adult', 'genres', 'popularity', 'original_language')
        # fields = '__all__'


class MovieRelatedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['tmdb_id', 'title', 'overview', 'release_date', 'poster_path']