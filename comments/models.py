from django.db import models
from django.conf import settings
from posts.models import Post

class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comentário de {self.owner.username} no Post #{self.post.id}"