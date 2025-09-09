# Copyright (c) 2025
# Yassine Fellous, Abdelkader Sofiane Ziri, Mathieu Duverne, Mohamed Marwane Bellagha
# Tous droits réservés. Utilisation interdite sans autorisation écrite des auteurs.

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView, 
    SpectacularRedocView
)

def home(request):
    html = """
    <h1>🚀 CDA Backend API</h1>
    <ul>
        <li><a href="/api/docs/">📖 Swagger UI Documentation</a></li>
        <li><a href="/api/redoc/">📚 ReDoc Documentation</a></li>
        <li><a href="/api/schema/">🔗 OpenAPI Schema</a></li>
        <li><a href="/installations/">🏟️ Installations</a></li>
        <li><a href="/auth/">🔐 Authentication</a></li>
        <li><a href="/signalements/">🚨 Signalements</a></li>
    </ul>
    """
    return HttpResponse(html)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Apps
    path('installations/', include('installations.urls')),
    path('auth/', include('authentication.urls')),
    path('signalements/', include('signalements.urls')),
    path('health/', include('authentication.urls')),
]