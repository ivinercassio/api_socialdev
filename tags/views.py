from rest_framework import viewsets, permissions
from .models import Tag, PostTag
from .serializers import TagSerializer, PostTagSerializer

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