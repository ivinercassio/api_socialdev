from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Midea
from .serializers import MideaSerializer

class MideaViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para a entidade MIDEA
    """
    queryset = Midea.objects.all()
    serializer_class = MideaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # Habilita o parse de arquivos Multipart, formulários e JSON
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], url_path='post')
    def by_post(self, request, pk=None):
        """
        GET /api/mideas/:id/post
        Retorna uma lista com todas as mídias associadas ao Post (:id)
        """
        post_mideas = Midea.objects.filter(post_id=pk)
        serializer = self.get_serializer(post_mideas, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='user')
    def profile_by_user(self, request, pk=None):
        """
        GET /api/mideas/:id/user
        Retorna a mídia da foto de perfil do Usuário (:id)
        """
        # Busca a mídia que pertence ao usuário informado e tem image_profile=True
        profile_midea = Midea.objects.filter(
            owner_id=pk, 
            image_profile=True
        ).first()

        if not profile_midea:
            return Response(
                {"detail": "Foto de perfil não encontrada para este usuário."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(profile_midea)
        return Response(serializer.data)