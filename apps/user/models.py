from django.db import models
from django.contrib.auth.hashers import make_password, check_password

class User(models.Model):

    TYPE_CHOICES = (
        ('CLIENT', 'client'),
        ('ADMIN', 'admin'),
    )

    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)                      
    public = models.BooleanField(default=True)
    about = models.TextField(max_length=300, blank=True, default='')
    tipo = models.CharField(
        max_length=6,
        choices=TYPE_CHOICES,
        default='CLIENT'                                                 
    )
    creation_date = models.DateTimeField(auto_now_add=True)          

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

    def __str__(self):
        return self.username

    # Cria o hash da senha e salva no campo 'password'
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    # Verifica se a senha informada bate com o hash salvo
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    # # Necessário para o DRF reconhecer o usuário como autenticado
    # @property
    # def is_authenticated(self):
    #     return True