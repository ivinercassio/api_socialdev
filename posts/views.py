from rest_framework import viewsets, permissions, status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F, Q

from .models import Post
from friends.models import Friend
from .serializers import PostSerializer
from .permissions import IsAuthenticatedForWriteOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para a entidade POST
    """
    queryset = Post.objects.all().order_by('-date_published')
    serializer_class = PostSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedForWriteOrReadOnly]

    def perform_create(self, serializer):
        # Associa automaticamente o usuário autenticado como autor do post
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'], url_path='user')
    def by_user(self, request, pk=None):
        """
        GET /api/posts/:id/user/
        Retorna uma lista com todos os posts do usuário cujo ID é o parâmetro :id
        """
        user_posts = Post.objects.filter(author_id=pk).order_by('-date_published')
        serializer = self.get_serializer(user_posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """
        PATCH /api/posts/:id/like/
        Incrementa +1 no número de curtidas de um post
        """
        post = self.get_object()
        post.like = F('like') + 1
        post.save(update_fields=['like'])
        post.refresh_from_db()
        return Response(self.get_serializer(post).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated])
    def unlike(self, request, pk=None):
        """
        PATCH /api/posts/:id/unlike/
        Decrementa -1 no número de curtidas de um post
        """
        post = self.get_object()
        if post.like > 0:
            post.like = F('like') - 1
            post.save(update_fields=['like'])
            post.refresh_from_db()
        return Response(self.get_serializer(post).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='friends', permission_classes=[permissions.IsAuthenticated])
    def friends_posts(self, request):
        """
        GET /api/posts/friends/
        Retorna posts apenas de usuários com os quais o usuário logado possui amizade.
        """
        current_user = request.user

        friendships = Friend.objects.filter(
            Q(friend_one=current_user) | Q(friend_two=current_user)
        )

        friend_ids = set()
        for friendship in friendships:
            if friendship.friend_one_id == current_user.id:
                friend_ids.add(friendship.friend_two_id)
            else:
                friend_ids.add(friendship.friend_one_id)

        posts = Post.objects.filter(author_id__in=friend_ids).order_by('-date_published')

        serializer = self.get_serializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)