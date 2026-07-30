from django.db import models
from django.conf import settings
from friends.models import Friend

class Message(models.Model):
    friend = models.ForeignKey(
        Friend,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    text = models.TextField()
    date_published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"De {self.from_user.username} para {self.to_user.username} ({self.date_published.strftime('%Y-%m-%d %H:%M')})"