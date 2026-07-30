from django.db import models
from posts.models import Post
from comments.models import Comment

class Report(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='reports',
        null=True,
        blank=True
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='reports',
        null=True,
        blank=True
    )
    date_report = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        target = f"Post #{self.post.id}" if self.post else f"Comentário #{self.comment.id}"
        return f"Denúncia do {target} em {self.date_report.strftime('%Y-%m-%d %H:%M')}"