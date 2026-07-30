from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # Tipos de Usuário
    class UserType(models.TextChoices):
        CLIENT = 'CLIENT', 'Client'
        ADMIN = 'ADMIN', 'Admin'

    username = models.CharField(max_length=150, unique=True)
    public = models.BooleanField(default=True)
    about = models.TextField(blank=True, null=True)
    type = models.CharField(
        max_length=20, 
        choices=UserType.choices, 
        default=UserType.CLIENT
    )
    creation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.username