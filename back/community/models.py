from django.db import models
from django.conf import settings
# Create your models here.

class Review(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  username = models.TextField()
  title = models.CharField(max_length=100)
  movie_title = models.CharField(max_length=50)
  rank = models.IntegerField()
  content = models.TextField()
  poster_path = models.TextField()
  created_at = models.DateTimeField(auto_now=True)
  updated_at = models.DateTimeField(auto_now_add=True)
  like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_reviews")
  hate_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="hate_reviews")
  
class Comment(models.Model):
  review = models.ForeignKey(Review,on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  content = models.CharField(max_length=200)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_comments")
  hate_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="hate_comments")