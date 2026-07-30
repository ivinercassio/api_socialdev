from rest_framework import viewsets, permissions
from .models import Comment
from .serializers import CommentSerializer

class CommentViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para a entidade COMMENT
    """
    queryset = Comment.objects.all().order_by('-date_published')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Atribui automaticamente o usuário logado como dono do comentário
        serializer.save(owner=self.request.user)