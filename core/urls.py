"""
URL configuration for core project.
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/users/', include('apps.user.urls')),
    # path('api/posts/', include('apps.post.urls')),
    # path('api/mideas/', include('apps.midea.urls')),
    # path('api/tags/', include('apps.tag.urls')),
    # path('api/post_tags/', include('apps.post_tag.urls')),
    # path('api/friends/', include('apps.friend.urls')),
    # path('api/messages/', include('apps.message.urls')),
    # path('api/comments/', include('apps.comment.urls')),
    # path('api/reports/', include('apps.report.urls')),

    # path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    # path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
