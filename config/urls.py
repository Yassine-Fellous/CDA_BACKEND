from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('installations.urls')),  # Préfixe API standard
]
#path('', include('api.urls', namespace='api'))