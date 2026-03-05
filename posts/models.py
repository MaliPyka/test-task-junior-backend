from django.db import models
from django.db.models.fields import DateTimeField


class Post(models.Model):
    """
    Модель для хранения постов, заруженных из Instagram
    """

    instagram_id = models.CharField(max_length=255, unique=True)
    owner = models.CharField(max_length=255)
    username = models.CharField(max_length=100)
    caption = models.TextField(null=True, blank=True)
    media_type = models.CharField(max_length=50)
    like_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    media_url = models.URLField(max_length=2500)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Post {self.instagram_id} by {self.username}"


class Comment(models.Model):
    """
    Модель для хранения коментариев, созданых с помощью Instagram API
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    instagram_id = models.CharField(max_length=255, unique=True)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment {self.instagram_id} text: {self.text}"
