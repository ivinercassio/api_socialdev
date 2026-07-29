from django.contrib.auth.backends import BaseBackend

from .models import User

# Backend de autenticação customizado para o model User
class AutenticacaoBackend(BaseBackend):

    # Autentica o usuário pelo campo 'username' e 'password'
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        
        if user.check_password(password):
            return user
        return None

    # Busca um usuário pelo ID
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
