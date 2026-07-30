from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Friend
from .serializers import FriendSerializer

class FriendViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para a entidade FRIEND
    """
    queryset = Friend.objects.all()
    serializer_class = FriendSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Associa automaticamente friend_one ao usuário autenticado
        serializer.save(friend_one=self.request.user)
    
    @action(detail=True, methods=['get'], url_path='user')
    def by_user(self, request, pk=None):
        """
        GET /api/friends/:id/user
        Retorna todas as relações de amizade do Usuário cujo ID é o parâmetro :id
        """
        user_friends = Friend.objects.filter(
            Q(friend_one_id=pk) | Q(friend_two_id=pk)
        )
        serializer = self.get_serializer(user_friends, many=True)
        return Response(serializer.data)