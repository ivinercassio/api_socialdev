from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    # 'author' será exibido como read_only para preenchermos automaticamente
    # com o usuário que fez a requisição
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Post
        fields = ['id', 'title', 'legend', 'author', 'author_username', 'like', 'date_published']
        read_only_fields = ['id', 'author', 'like', 'date_published']