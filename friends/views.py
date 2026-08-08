from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Friend, FriendRequest
from .serializers import FriendSerializer, FriendRequestSerializer

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

class FriendRequestViewSet(viewsets.ModelViewSet):
    queryset = FriendRequest.objects.all().order_by('-date_request')
    serializer_class = FriendRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user_one=self.request.user)

    @action(detail=True, methods=['get'], url_path='user')
    def by_user(self, request, pk=None):
        """
        GET /api/friend_requests/:id/user/
        Retorna apenas as solicitações de amizade RECEBIDAS pelo usuário (:id)
        """
        # Filtra apenas onde o usuário do parâmetro :id é o destinatário (user_two)
        received_requests = FriendRequest.objects.filter(
            user_two_id=pk
        ).order_by('-date_request')

        serializer = self.get_serializer(received_requests, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='accept')
    def accept_request(self, request, pk=None):
        """
        POST /api/friend_requests/:id/accept/
        Exclui a solicitação de amizade e cria uma nova amizade atomicamente.
        """
        # Garante que a solicitação existe e que o usuário logado é o destinatário (user_two)
        friend_request = get_object_or_404(FriendRequest, pk=pk, user_two=request.user)

        # Inicia a transação atômica no banco de dados
        with transaction.atomic():
            # 1. Cria o registro de amizade
            friendship = Friend.objects.create(
                friend_one=friend_request.user_one,
                friend_two=friend_request.user_two
            )

            # 2. Exclui a solicitação de amizade
            friend_request.delete()

        # Serializa e retorna a nova amizade criada
        serializer = FriendSerializer(friendship, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)