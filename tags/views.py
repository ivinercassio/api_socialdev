from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Tag, PostTag
from .serializers import TagSerializer, PostTagSerializer
from posts.serializers import PostSerializer

class TagViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para a entidade TAG
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PostTagViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para a entidade POST_TAG
    """
    queryset = PostTag.objects.all()
    serializer_class = PostTagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    @action(detail=True, methods=['get'], url_path='tag')
    def posts_by_tag(self, request, pk=None):
        """
        GET /api/post_tags/:id/tag
        Retorna todos os posts associados à Tag cujo ID é o parâmetro :id
        """
        # Filtra os vínculos PostTag pelo ID da Tag e extrai os Posts associados
        post_tags = PostTag.objects.filter(tag_id=pk).select_related('post')
        posts = [pt.post for pt in post_tags]
        
        # Serializa e retorna a lista de Posts
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='post')
    def tags_by_post(self, request, pk=None):
        """
        GET /api/post_tags/:id/post
        Retorna todas as tags associadas ao Post cujo ID é o parâmetro :id
        """
        # Filtra os vínculos PostTag pelo ID do Post e extrai as Tags associadas
        post_tags = PostTag.objects.filter(post_id=pk).select_related('tag')
        tags = [pt.tag for pt in post_tags]
        
        # Serializa e retorna a lista de Tags
        serializer = TagSerializer(tags, many=True, context={'request': request})
        return Response(serializer.data)