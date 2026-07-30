from django.db import models
from django.conf import settings

class Post(models.Model):
    title = models.CharField(max_length=150)
    legend = models.TextField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='posts'
    )
    like = models.IntegerField(default=0)
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"POST: {self.title} por {self.author.username}"