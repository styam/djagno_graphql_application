from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone



class Post(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now())
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} {self.description} {self.publish_date} {self.author}"


class Comment(models.Model):
    connected_post = models.ForeignKey(Post, related_name='Comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField()
    date_of_comment = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return f"{self.connected_post} {self.author} {self.comments} {self.date_of_comment}"
