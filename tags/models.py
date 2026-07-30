from django.db import models
from posts.models import Post

class Tag(models.Model):
    theme = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"#{self.theme}"


class PostTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='post_tags')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_tags')

    class Meta:
        # Garante que não teremos duplicidade do mesmo par (tag, post)
        unique_together = ('tag', 'post')

    def __str__(self):
        return f"Post #{self.post.id} - Tag: {self.tag.theme}"