from rest_framework import viewsets, permissions
from .models import Message
from .serializers import MessageSerializer

class MessageViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para a entidade MESSAGE
    """
    queryset = Message.objects.all().order_by('-date_published')
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Associa automaticamente from_user ao usuário autenticado
        serializer.save(from_user=self.request.user)