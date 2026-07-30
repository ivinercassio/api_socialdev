from rest_framework import viewsets, permissions
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