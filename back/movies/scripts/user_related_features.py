import random
from faker import Faker
from movies.models import Movie
from community.models import Review, Comment

from django.contrib.auth import get_user_model

User = get_user_model()
fake = Faker()
target = 100


def run():
    """
    movies.model의 유저 관련 기능 스크립트
    - 영화별 리뷰 생성 및 리뷰별 좋아요 설정
    - 리뷰별 댓글 생성 및 댓글별 좋아요 설정
    """

    for movie in Movie.objects.all():
        # 영화별 좋아요 0~10개
        for i in random.sample(range(1, target + 1), random.randint(0, 10)):
            movie_like_user = User.objects.get(pk=i)
            if movie_like_user not in movie.like_users.all():
                movie.like_users.add(movie_like_user)
                print(f"{movie}: Added to User {movie_like_user} likes")
        # 영화별 싫어요 0~10개
        for i in random.sample(range(1, target + 1), random.randint(0, 10)):
            movie_hate_user = User.objects.get(pk=i)
            if movie_hate_user not in movie.hate_users.all():
                movie.hate_users.add(movie_hate_user)
                print(f"{movie}: Added to User {movie_hate_user} hates")
        # 영화별 찜 0~10개
        for i in random.sample(range(1, target + 1), random.randint(0, 10)):
            movie_favorite_user = User.objects.get(pk=i)
            if movie_favorite_user not in movie.favorite_users.all():
                movie.favorite_users.add(movie_favorite_user)
                print(f"{movie}: Added to User {movie_favorite_user} favorites")
        # 영화별 리뷰 0~5개
        for i in range(random.randint(0, 5)):
            review_user = User.objects.get(pk=random.randint(1, target))
            review = Review.objects.create(
                user=review_user,
                username=review_user.username,
                movie_title=movie.title,
                title=fake.sentence(nb_words=10),
                content=fake.paragraph(nb_sentences=5),
                poster_path=movie.poster_path,
                rank=round(random.uniform(0, 5), 1),
            )
            print(f"Created {review} by {review_user} @ {movie}")

            # 각 리뷰별 좋아요 0~5개
            for i in random.sample(range(1, target + 1), random.randint(0, 5)):
                review_like_user = User.objects.get(pk=i)
                if review.user == review_like_user:
                    continue

                if review_like_user not in review.like_users.all():
                    review.like_users.add(review_like_user)
                    print(f"  {review}: Added to User {review_like_user} likes")
                    
            # 각 리뷰별 싫어요 0~5개
            for i in random.sample(range(1, target + 1), random.randint(0, 5)):
                review_hate_user = User.objects.get(pk=i)
                if review.user == review_hate_user:
                    continue

                if review_hate_user not in review.hate_users.all():
                    review.hate_users.add(review_hate_user)
                    print(f"  {review}: Added to User {review_hate_user} hates")

            # 리뷰별 댓글 0~5개
            for i in range(random.randint(0, 5)):
                comment_user = User.objects.get(pk=random.randint(1, target))
                comment = Comment.objects.create(
                    user=comment_user,
                    review=review,
                    content=fake.paragraph(nb_sentences=5),
                )
                print(f"    Created {comment} by {comment_user} @ {review}")

                # 각 댓글별 좋아요 0~5개
                for i in random.sample(range(1, target + 1), random.randint(0, 5)):
                    comment_like_user = User.objects.get(pk=i)
                    if comment.user == comment_like_user:
                        continue

                    if comment_like_user not in comment.like_users.all():
                        comment.like_users.add(comment_like_user)
                        print(f"      {comment}: Added to User {comment_like_user} likes")
                # 각 댓글별 싫어요 0~5개
                for i in random.sample(range(1, target + 1), random.randint(0, 5)):
                    comment_hate_user = User.objects.get(pk=i)
                    if comment.user == comment_hate_user:
                        continue

                    if comment_hate_user not in comment.hate_users.all():
                        comment.hate_users.add(comment_hate_user)
                        print(f"      {comment}: Added to User {comment_hate_user} hates")
        print()
