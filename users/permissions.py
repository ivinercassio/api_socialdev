from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão que permite apenas ao dono do objeto editá-lo.
    """
    def has_object_permission(self, request, view, obj):
        # Leitura é liberada (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True

        # Escrita (PUT, PATCH, DELETE) apenas para o próprio usuário
        return obj == request.user