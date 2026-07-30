from rest_framework import viewsets, permissions
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para a entidade POST
    """
    queryset = Post.objects.all().order_by('-date_published')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Associa automaticamente o usuário autenticado como autor do post
        serializer.save(author=self.request.user)