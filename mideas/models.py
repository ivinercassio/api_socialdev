from django.db import models
from django.conf import settings
from posts.models import Post

class Midea(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mideas'
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='mideas',
        null=True,
        blank=True
    )
    image_profile = models.BooleanField(default=False)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/', null=True, blank=True)
    link = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f"Mídia #{self.id} do usuário {self.owner.username}"