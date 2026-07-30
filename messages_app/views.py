from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
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

    @action(detail=True, methods=['get'], url_path='friend')
    def by_friend(self, request, pk=None):
        """
        GET /api/messages/:id/friend
        Retorna todas as mensagens trocadas no chat de uma amizade específica (:id)
        """
        # Filtra as mensagens associadas ao ID da relação de amizade (Friend)
        friend_messages = Message.objects.filter(friend_id=pk).order_by('date_published')
        
        serializer = self.get_serializer(friend_messages, many=True)
        return Response(serializer.data)