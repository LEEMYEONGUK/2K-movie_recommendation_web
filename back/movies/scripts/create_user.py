import random
from faker import Faker
from django.contrib.auth import get_user_model
from movies.models import Genre

User = get_user_model()
fake = Faker()
target = 100
genres = [
    12,
    14,
    16,
    18,
    27,
    28,
    35,
    36,
    37,
    53,
    80,
    99,
    878,
    9648,
    10402,
    10749,
    10751,
    10752,
    10770,
]


def run():
    """
    더미 유저 생성 스크립트
    필수 조건: loaddata of genres.json, movies.json
    """
    # 유저 생성
    for i in range(1, target + 1):
        if User.objects.filter(username=f"fakeruser{i}"):
            continue

        user = User.objects.create_user(
            username=f"fakeruser{i}",
            password="2w2w1q1q",
        )
        print(f"Created User {i}")

        # 3개 이상의 선호 장르 선택
        # for genre_pk in random.sample(genres, random.randint(3, len(genres))):
        #     genre = Genre.objects.get(pk=genre_pk)
        #     user.liked_genres.add(genre)
        #     print(f"  Added {genre} to {user} likes")
    print()

    # 팔로우 관계 설정
    # for i in range(1, target + 1):
    #     user_to = User.objects.get(pk=i)
    #     for follower in random.sample(range(1, target + 1), random.randint(0, 5)):
    #         if i == follower:
    #             continue
    #         else:
    #             user_from = User.objects.get(pk=follower)
    #             user_to.followers.add(user_from)
    #             print(f"User {i}: Added user {follower} to follower list")
