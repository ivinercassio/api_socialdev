from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'public', 'about', 'type', 'creation_date']
        read_only_fields = ['id', 'type', 'creation_date']

    def create(self, validated_data):
        # Criptografa a senha adequadamente ao criar o usuário
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            public=validated_data.get('public', True),
            about=validated_data.get('about', ''),
            type=validated_data.get('type', User.UserType.CLIENT),
        )
        return user