from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
from .models import User
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework.views import APIView
from rest_framework import status

# 전체 유저 정보 조회
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def user(request):
  if request.method == 'GET':
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

# 로그인된 유저 정보 조회(id로 불러오기)
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def user_profile(request, user_pk):
  if request.method == 'GET':
    review = User.objects.get(pk=user_pk)
    serializer = UserSerializer(review)
    return Response(serializer.data)


# 로그인된 유저 정보 조회
@api_view(['GET',])
@permission_classes([IsAuthenticated])
def user_detail(request, username):
  if request.method == 'GET':
    review = User.objects.get(username=username)
    serializer = UserSerializer(review)
    return Response(serializer.data)