from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

# Serializer do login: valida usuario + senha e gera tokens JWT
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)                          

    def validate(self, data):
        from django.contrib.auth import authenticate
        user = authenticate(
            request=self.context.get('request'),
            username=data['username'],
            password=data['password']
        )
        if not user:
            raise serializers.ValidationError('Credenciais inválidas.')
        self.user = user
        return data

    def get_tokens(self):
        refresh = RefreshToken.for_user(self.user)
        return {
            'access': str(refresh.access_token), # 60 min
            'refresh': str(refresh), # 7 days
        }


# Serializer CRUD
class UserCRUDSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, required=False)   

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'public', 'about', 'tipo', 'creation_date']
        read_only_fields = ['id', 'creation_date']  

    def validate_username(self, value):
        instance = self.instance
        if User.objects.filter(username=value).exclude(pk=getattr(instance, 'pk', None)).exists():
            raise serializers.ValidationError('Este username de usuário já está em uso.')
        return value

    def validate_tipo(self, value):
        """Regra 1: Qualquer um cria CLIENT. Apenas ADMIN cria ADMIN."""
        request = self.context.get('request')
        if value == 'ADMIN':
            # Se o usuário não estiver logado ou não for ADMIN, bloqueia
            if not request or not request.user or not request.user.is_authenticated or request.user.tipo != 'ADMIN':
                raise serializers.ValidationError('Apenas administradores podem criar ou definir usuários como ADMIN.')
        return value

    def validate(self, data):
        """Regra 3: Qualquer usuário só pode alterar/atualizar a si próprio."""
        request = self.context.get('request')
        
        # Verifica se é uma operação de atualização (PUT/PATCH)
        if self.instance and request:
            user_logado = request.user
            
            # Se não for ADMIN e estiver tentando alterar outro usuário, bloqueia
            if user_logado.tipo != 'ADMIN' and self.instance.id != user_logado.id:
                raise serializers.ValidationError('Você não tem permissão para alterar os dados de outro usuário.')
                
            # Impede que um não-admin mude o próprio tipo para ADMIN na atualização
            if user_logado.tipo != 'ADMIN' and data.get('tipo') == 'ADMIN':
                raise serializers.ValidationError('Você não pode alterar seu próprio perfil para ADMIN.')

        return data
    
    def create(self, validated_data):
        # Garante que a senha seja obrigatória apenas na criação
        if 'password' not in validated_data:
            raise serializers.ValidationError({'password': 'Este campo é obrigatório para novos registros.'})
            
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
