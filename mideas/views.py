from rest_framework import viewsets, permissions
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