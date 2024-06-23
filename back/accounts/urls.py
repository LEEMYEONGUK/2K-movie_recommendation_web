from django.urls import path
from . import views

urlpatterns = [
    path('', views.user),
    path('<int:user_pk>/', views.user_profile),
    path('<str:username>/', views.user_detail)
]



