from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import MovieListSerializer, MovieSerializer, GenreListSerializer,GenreMoviesSerializer, MovieReadSerializer,MovieRelatedSerializer
from .models import Movie,Genre
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework import status
from .utils import fetch_and_save_movies, fetch_and_save_genres, delete_movies_without_trailers, get_movies_related
from accounts.models import User
from datetime import datetime
import random
import requests
from django.conf import settings

TOKEN = settings.TOKEN

# 영화 리스트 조회
@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def movie_list(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie.objects.order_by('-popularity')[:30])
        serializers = MovieListSerializer(movies, many=True)
        return Response(serializers.data)
    elif request.method == 'POST':
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data)

# 영화 상세 정보 조회
@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def movie_detail(request, movie_pk):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

# 장르 리스트 조회
@api_view(['GET'])
def genre_list(request):
    if request.method == 'GET':
        genres = get_list_or_404(Genre)
        serializers = GenreListSerializer(genres, many=True)
        return Response(serializers.data)

# 장르별 영화 분류
@api_view(['GET'])
def filter_genre(request, genre_pk):
    if request.method == 'GET':
        movies = get_list_or_404(Movie.objects.order_by('-popularity'), genres = genre_pk)
        serializers = MovieListSerializer(movies, many=True)
        return Response(serializers.data)
    
# 영화 좋아요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_likes(request, movie_pk, user_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = get_object_or_404(User, pk=user_pk)
    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        like = False
    else:
        movie.like_users.add(user)
        like = True
    like_status = {
        'liked': like,
        'count': movie.like_users.count(),
    }
    return JsonResponse(like_status)

# 영화 싫어요
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_hates(request, movie_pk, user_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = get_object_or_404(User, pk=user_pk)
    if movie.hate_users.filter(pk=user.pk).exists():
        movie.hate_users.remove(user)
        hate = False
    else:
        movie.hate_users.add(user)
        hate = True
    hate_status = {
        'hated': hate,
        'count': movie.hate_users.count(),
    }
    return JsonResponse(hate_status)


# 영화 찜하기 설정
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def movie_favorite(request, movie_pk, user_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = get_object_or_404(User, pk=user_pk)
    if movie.favorite_users.filter(pk=user.pk).exists():
        movie.favorite_users.remove(user)
        favorite = False
    else:
        movie.favorite_users.add(user)
        favorite = True
    favorite_status = {
        'favorited': favorite,
        'count': movie.favorite_users.count(),
    }
    return JsonResponse(favorite_status)

# 좋아요, 싫어요, 찜하기 현재 유저의 상태(유저 본인, 아니면 로그아웃 상태) 조회 및 적용
@api_view(['GET'])
def read_lhf(request,movie_pk, user_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = get_object_or_404(User, pk=user_pk)
    if movie.favorite_users.filter(pk=user.pk).exists():
        favorite = True
    else:
        favorite = False
    if movie.hate_users.filter(pk=user.pk).exists():
        hate = True
    else:
        hate = False
    if movie.like_users.filter(pk=user.pk).exists():
        like = True
    else:
        like = False
    lhf_status = {
        'liked': like,
        'hated': hate,
        'favorited': favorite,
        'like_count': movie.like_users.count(),
        'hate_count': movie.hate_users.count(),
    }
    return JsonResponse(lhf_status)


#요일별 추천 페이지 구현
@api_view(['GET'])
def today_recommend(request):
    movies = []
    # 현재 날짜와 시간 가져오기
    now = datetime.now()
    # 요일을 문자열로 변환 (예: 'Monday', 'Tuesday', ...)
    today_weekday = now.strftime('%A')
    # 지피티 추천
    # 월요일 : 지친하루 피로룰 풀기 위해 코미디, 드라마
    if today_weekday == 'Monday':
        today_genres = [18, 35]
    # 화요일 : 주의 초반으로 어느정도 긴장감을 주는 SF, 공포
    elif today_weekday == 'Tuesday':
        today_genres = [27, 878]
    # 수요일 : 주 중반으로 활력을 줄 수 있는 액션, 전쟁
    elif today_weekday == 'Wednesday':
        today_genres = [28, 10752]
    # 목요일 : 조금 더 가벼운 즐거움을 주는 미스터리, 판타지
    elif today_weekday == 'Thursday':
        today_genres = [9648, 14]
    # 금요일 : 불금의 시작, 로멘스와 모험, 스릴러, 범죄
    elif today_weekday == 'Friday':
        today_genres = [10749, 12, 53, 80]
    # 토요일 : 가족들과 함께 즐길 수 있는 애니메이션, 가족, 음악
    elif today_weekday == 'Saturday':
        today_genres = [16, 10751, 10402]
    # 일요일 : 가볍게 지식을 얻으며 휴식할 수 있는 다큐멘터리, 역사
    elif today_weekday == 'Sunday':
        today_genres = [99, 36]
    # for genre in today_genres:
    #     genre_movies = get_list_or_404(Movie, genres=genre)
    #     movies.extend(genre_movies)
    # movies = sorted(movies, key=lambda x: x.popularity, reverse=True)[:10]
    movies = get_list_or_404(Movie.objects.filter(genres__in=today_genres))
    movies = list(set(movies))
    movies = sorted(movies, key=lambda x: x.vote_average, reverse=True)[:9]
    serializers = MovieListSerializer(movies, many=True)
    return Response(serializers.data)

# 한국 영화 추천 : 최신 인기작
@api_view(['GET'])
def korean_movies(request):
    movies = get_list_or_404(Movie, original_language = 'ko')
    movies = sorted(movies, key=lambda x: (x.popularity, x.release_date), reverse=True)
    movies = movies[:18]
    serializers = MovieListSerializer(movies, many=True)
    return Response(serializers.data)

# 이번 주 추천 작품
@api_view(['GET'])
def week_recommend(request):
    movies = get_list_or_404(Movie.objects.order_by('-popularity')[:200])
    movies = random.sample(movies, 27)
    serializers = MovieListSerializer(movies, many=True)
    return Response(serializers.data)


# 좋아요 한 장르 별 영화 가져오기
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def liked_genres_with_movies(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    liked_movies = user.like_movies.all()
    genres_dict = {}
    for movie in liked_movies:
        for genre in movie.genres.all():
            if genre not in genres_dict:
                genres_dict[genre] = []
    
    for genre in genres_dict:
        genre_movies = Movie.objects.filter(genres=genre).order_by('-popularity')[:27]
        genres_dict[genre] = genre_movies

    data = {genre.name:
            GenreMoviesSerializer({'genre': genre, 'movies': movies}).data
            for genre, movies in genres_dict.items()}
    return Response(data)


# 좋아요 기준 유저에게 추천하는 영화 목록
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_recommend(request, user_pk):
    user = get_object_or_404(User, pk=user_pk)
    liked_movies = user.like_movies.all()
    
    genres = []

    for movie in liked_movies:
        for genre in movie.genres.all():
            if genre not in genres:
                genres.append(genre)
    
    movies = get_list_or_404(Movie.objects.filter(genres__in=genres))
    movies = list(set(movies))
    movies = sorted(movies, key=lambda x: x.popularity, reverse=True)[:27]
    serializers = MovieListSerializer(movies, many=True)
    return Response(serializers.data)


# 나의 찜 목록 조회
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def my_favorite(request, user_pk):
    if request.method == 'GET':
        movies = Movie.objects.filter(favorite_users=user_pk)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

# 프로필 찜한 영화 가져오기
# serializer 는 있는거 사용!
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def profile_favorite(request, user_pk):
    if request.method == 'GET':
        movies = Movie.objects.filter(favorite_users=user_pk)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


@api_view(['GET',])
@permission_classes([IsAuthenticated])
def profile_like(request, user_pk):
    if request.method == 'GET':
        movies = Movie.objects.filter(like_users=user_pk)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

# 검색 기능
# 혹시 더 필요한 항목 있으면 results에 추가하기!
def search(request):
    print(request)
    query = request.GET.get('query', '')
    if query:
        movies = Movie.objects.filter(title__icontains=query)
        results = [{
            'tmdb_id': movie.tmdb_id,
            'title': movie.title,
            'overview': movie.overview,
            'poster_path': movie.poster_path,
            'backdrop_path': movie.backdrop_path,
            'genres': [genre.name for genre in movie.genres.all()],
            } for movie in movies]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})


@api_view(['GET'])
def related_movies(request, movie_pk):
    url = f"https://api.themoviedb.org/3/movie/{movie_pk}/recommendations?language=ko-KR&page=1"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        api_movies = response.json().get('results', [])
        tmdb_ids = [movie['id'] for movie in api_movies]
        
        matching_movies = Movie.objects.filter(tmdb_id__in=tmdb_ids)
        serializer = MovieSerializer(matching_movies, many=True)
        
        return Response(serializer.data)
    else:
        return Response({"error": "Failed to fetch data from the API"}, status=response.status_code)


# TMDB에서 장르 가져오기 위한 view함수
class FetchGenresAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            fetch_and_save_genres()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
# TMDB에서 영화 정보 가져오기 위한 view 함수
class FetchMoviesAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            fetch_and_save_movies()
            delete_movies_without_trailers()
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)