from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MideaViewSet

router = DefaultRouter()
router.register(r'mideas', MideaViewSet, basename='midea')

urlpatterns = [
    path('', include(router.urls)),
]