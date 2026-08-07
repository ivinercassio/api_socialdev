from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FriendViewSet, FriendRequestViewSet

router = DefaultRouter()
router.register(r'friends', FriendViewSet, basename='friend')
router.register(r'friend_requests', FriendRequestViewSet, basename='request')

urlpatterns = [
    path('', include(router.urls)),
]