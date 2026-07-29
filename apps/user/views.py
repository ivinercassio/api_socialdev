# Views: endpoints da API de users
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .permissions import IsAdmin, IsClient
from .serializers import LoginSerializer, UserCRUDSerializer


# GET, POST /api/usuarios/ - Lista usuários (só ADMIN) ou cria usuários (Qualquer um cria CLIENT, só ADMIN cria ADMIN)
class UserListCreateView(APIView):
    def get_permissions(self):
        """Define permissões dinâmicas: POST é público (registro), GET exige autenticação."""
        if self.request.method == 'POST':
            return [AllowAny()]
        return [IsAuthenticated()]

    def get(self, request):
        """Apenas o usuário ADMIN pode consultar a lista com todos os usuários."""
        if request.user.tipo != 'ADMIN':
            return Response(
                {'detail': 'Você não tem permissão para listar todos os usuários.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        usuarios = User.objects.all()
        serializer = UserCRUDSerializer(usuarios, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request):
        """Permite que qualquer pessoa crie um CLIENT. Criação de ADMIN é validada no Serializer."""
        serializer = UserCRUDSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        usuario = serializer.save()
        
        # Gera o token JWT automaticamente após o cadastro bem-sucedido
        refresh = RefreshToken.for_user(usuario)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'usuario': {
                'id': usuario.id,
                'username': usuario.username,
                'tipo': usuario.tipo,
            }
        }, status=status.HTTP_201_CREATED)


# POST /api/auth/login/ - Faz login e retorna tokens JWT (público)
class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        # Recupera o usuário validado guardado no serializer
        user = serializer.user
        tokens = serializer.get_tokens()
        
        return Response({
            **tokens,
            'usuario': {
                'id': user.id,
                'username': user.username,
                'tipo': user.tipo,
            }
        }, status=status.HTTP_200_OK)


# POST /api/auth/logout/ - Faz logout (qualquer usuário autenticado)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Nota: Se quiser invalidar o token no backend, adicione o refresh_token no request.data 
        # e faça: RefreshToken(request.data['refresh']).blacklist()
        return Response({'mensagem': 'Logout realizado com sucesso.'}, status=status.HTTP_200_OK)


# GET/PUT/DELETE /api/usuarios/{id}/ - Detalhes e edição (Próprio usuário ou ADMIN). Exclusão (Só o próprio ou ADMIN).
class UsuarioDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        """Permite consulta se o usuário for ADMIN ou se estiver consultando a si próprio."""
        usuario = self.get_object(pk)
        if usuario is None:
            return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
            
        # Regra de Consulta: Se não for ADMIN e tentar olhar outra ID, bloqueia
        if request.user.tipo != 'ADMIN' and request.user.id != usuario.id:
            return Response(
                {'detail': 'Você não tem permissão para visualizar o perfil de outro usuário.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        serializer = UserCRUDSerializer(usuario, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        """Qualquer usuário pode atualizar apenas a si próprio (Validado no Serializer)."""
        usuario = self.get_object(pk)
        if usuario is None:
            return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
            
        # O UserCRUDSerializer já bloqueia edições cruzadas no método validate(), 
        # mas adicionamos esta trava na View para retornar o HTTP 403 explicitamente.
        if request.user.tipo != 'ADMIN' and request.user.id != usuario.id:
            return Response(
                {'detail': 'Você não tem permissão para alterar os dados de outro usuário.'}, 
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = UserCRUDSerializer(usuario, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        """Garante que um usuário comum possa excluir apenas a sua própria conta."""
        usuario = self.get_object(pk)
        if usuario is None:
            return Response({'detail': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
            
        if request.user.tipo != 'ADMIN' and request.user.id != usuario.id:
            return Response(
                {'detail': 'Você não tem permissão para excluir outro usuário.'}, 
                status=status.HTTP_403_FORBIDDEN
            )
            
        usuario.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
