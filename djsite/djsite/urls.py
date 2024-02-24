"""
URL configuration for djsite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.decorators.cache import cache_page

from djsite import settings
from women import views
from women.sitemaps import PostSitemap, CategorySitemap
from women.views import page_not_found
from django.contrib.sitemaps.views import sitemap
from women.models import Women

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

# router = routers.DefaultRouter() # или кастомный MyCustomRouter из routers.py
# router.register(r"women", views.WomenViewSet, basename='women')

sitemaps = {
    'posts': PostSitemap,
    'cats': CategorySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('women.urls')),
    path('users/', include('users.urls', namespace="users")),
    path("__debug__/", include("debug_toolbar.urls")),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('captcha/', include('captcha.urls')),
    path('sitemap.xml', cache_page(86400)(sitemap), {'sitemaps': sitemaps}, name="django.contrib.sitemaps.views.sitemap"),
    # path("api/v1/", include(router.urls)),
    path('api/v1/drf-auth/', include('rest_framework.urls')), # аутентификация по сессиям
    path("api/v1/women/", views.WomenAPIList.as_view()),
    path("api/v1/women/<int:pk>/", views.WomenAPIUpdate.as_view()),
    path("api/v1/womendelete/<int:pk>/", views.WomenAPIDelete.as_view()),
    path('api/v1/auth/', include('djoser.urls')),          # аутентификация по токенам
    re_path(r'^auth/', include('djoser.urls.authtoken')),  # аутентификация по токенам
    path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # аутентификация JWT по токенам (создание)
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), # аутентификация JWT по токенам (обновление)
    path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'), # аутентификация по JWT токенам (проверка подписи)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
admin.site.site_header = "Панель администрирования"
admin.site.index_title = "Известные женщины мира"
