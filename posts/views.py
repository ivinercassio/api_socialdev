from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(detail=True, methods=['get'], url_path='user')
    def by_user(self, request, pk=None):
        """
        GET /api/posts/:id/user
        Retorna uma lista com todos os posts do usuário cujo ID é o parâmetro :id
        """
        # Aqui 'pk' representa o ID do usuário recebido na URL
        user_posts = Post.objects.filter(author_id=pk).order_by('-date_published')
        
        # Passamos context={'request': request} para garantir URLs completas (ex: mídias se houver)
        serializer = self.get_serializer(user_posts, many=True)
        return Response(serializer.data)