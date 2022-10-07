"""chat_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
import environ
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from apps.users.views import CustomTokenObtainPairView

env = environ.Env()

def get_swagger_permission_class():
    if env.bool('DEBUG', default=False):
        return [AllowAny]

    return [IsAuthenticated]

schema_view = get_schema_view(
    openapi.Info(
        title='Chat app API',
        default_version='v1',
        description='',
        terms_of_service='',
        contact=openapi.Contact(email='contact@snippets.local'),
        license=openapi.License(name='BSD License'),
    ),
    public=env.bool('DEBUG', default=False),
    permission_classes=get_swagger_permission_class(),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # App urls.
    path('api/users/', include('apps.users.urls', namespace='users')),
    path('api/chats/', include('apps.chats.urls', namespace='chats')),


    # JWT token urls.
    path('api/token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # password reset url.
    path('api/password-reset/',
         include('django_rest_passwordreset.urls', namespace='password_reset')),

    # Swagger urls.
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'^redoc/$', schema_view.with_ui('redoc',
                                         cache_timeout=0), name='schema-redoc'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if env.bool('DEBUG', default=False):
    import debug_toolbar
    urlpatterns.append(
        path('__debug__/', include(debug_toolbar.urls)),
    )
