from rest_framework import serializers
from .models import Review, Comment
from accounts.models import User

# 리뷰 전체 조회
class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # fields = '__all__'
        fields = ('id', 'title', 'movie_title', 'rank', 'content', 'user', 'poster_path', 'username')

# 리뷰 작성
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        # fields = '__all__'
        fields = ('title', 'movie_title', 'rank', 'content', 'user', 'poster_path', 'username')
        read_only_fielsds = ('user',)

# 리뷰 상세 정보 조회
class ReviewDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

# 리뷰 <- 댓글 조회
class CommentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

# 리뷰 <- 댓글 작성
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('review', 'user', 'content',)
        read_only_fielsds = ('user','review')

# class ReviewSerializer(serializers.ModelSerializer):    
#     class Meta:
#         model = Review
#         fields = ('tmdb_id', 'title', 'overview','release_date','poster_path','vote_count','vote_average','backdrop_path', 'adult', 'genres', 'popularity')
        # fields = '__all__'
