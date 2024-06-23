from django.urls import path
from . import views

urlpatterns = [
    # 전체 리뷰 조회 및 리뷰 생성
    path("reviews/", views.review_list),
    # 리뷰 상세 정보
    path("<int:review_pk>/", views.review_detail),
    # 리뷰 좋아요
    path("<int:review_pk>/like/<int:user_pk>/", views.review_like),
    # 리뷰 싫어요
    path("<int:review_pk>/hate/<int:user_pk>/", views.review_hate),
    # 리뷰 <- 댓글 작성, 조회
    path("<int:review_pk>/comment/", views.review_comment),
    # 리뷰 <- 상세 조회, 삭제
    path('<int:review_pk>/comment/<int:comment_pk>/', views.review_comment_detail),
    # 리뷰 - 댓글 좋아요
    path(
        "<int:review_pk>/comment/<int:comment_pk>/like/<int:user_pk>/",
        views.review_comment_like,
    ),
    # 리뷰 - 댓글 싫어요
    path(
        "<int:review_pk>/comment/<int:comment_pk>/hate/<int:user_pk>/",
        views.review_comment_hate,
    ),
    # 유저의 리뷰 찾기
    path('reviews/<int:user_pk>/', views.user_review),
    # 영화의 리뷰 찾기
    path('reviews/<str:movie_title>/', views.movie_review),
]
