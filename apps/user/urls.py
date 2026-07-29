from django.urls import path

from .views import LoginView, LogoutView, UserListCreateView, UsuarioDetailView

urlpatterns = [
    # Autenticação
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    
    # Endpoints de Usuários (Centralizados)
    path('', UserListCreateView.as_view(), name='user-list-create'),
    path('<int:pk>/', UsuarioDetailView.as_view(), name='user-detail'),
]
