from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(detail=True, methods=['get'], url_path='post')
    def by_post(self, request, pk=None):
        """
        GET /api/comments/:id/post
        Retorna todos os comentários associados ao Post cujo ID é o parâmetro :id
        """
        post_comments = Comment.objects.filter(post_id=pk).order_by('-date_published')
        serializer = self.get_serializer(post_comments, many=True)
        return Response(serializer.data)