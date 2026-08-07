from rest_framework import permissions

class IsAuthenticatedForWriteOrReadOnly(permissions.BasePermission):
    """
    Permite leitura pública (GET, HEAD, OPTIONS), 
    mas exige que o usuário esteja autenticado para modificações (PATCH, PUT, DELETE).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated