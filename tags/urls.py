from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TagViewSet, PostTagViewSet

router = DefaultRouter()
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'post_tags', PostTagViewSet, basename='posttag')

urlpatterns = [
    path('', include(router.urls)),
]