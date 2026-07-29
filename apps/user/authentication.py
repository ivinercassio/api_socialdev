from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User

# Autenticação JWT customizada para buscar users na tabela 'users'
class JWTAuthenticationCustom(JWTAuthentication):
    
    # Sobrescreve o método para buscar o user
    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
