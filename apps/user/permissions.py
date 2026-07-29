from rest_framework.permissions import BasePermission

# Permissoes: regras de acesso dos endpoints

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.tipo == 'ADMIN'

class IsClient(BasePermission):
    """Bloqueia usuários CLIENT de acessar relatórios e deletar comentários."""
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.tipo != 'CLIENT':
            return True

        # CLIENT nao tem acessso aos endpoints abaixo
        if request.path.startswith('/api/reports/'):
            return False
        if request.method == 'DELETE' and '/api/comments/' in request.path:
            return False

        url_user_id = view.kwargs.get('pk')

        if '/api/users/' in request.path:
            if request.method == 'GET' and not url_user_id:
                return False

            if request.method in ['PUT', 'PATCH', 'DELETE']:
                if not url_user_id or str(request.user.id) != str(url_user_id):
                    return False

        return True
