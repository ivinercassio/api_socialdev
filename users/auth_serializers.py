from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserSerializer 

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        # Adiciona o objeto do usuário na resposta do Login
        user_serializer = UserSerializer(self.user)
        
        # Estrutura a resposta customizada
        return {
            "access": data["access"],
            "refresh": data["refresh"],
            "user": user_serializer.data
        }