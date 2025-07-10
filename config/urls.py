# Copyright (c) 2025
# Yassine Fellous, Abdelkader Sofiane Ziri, Mathieu Duverne, Mohamed Marwane Bellagha
# Tous droits réservés. Utilisation interdite sans autorisation écrite des auteurs.

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("Bienvenue sur l'API CDA Backend !")

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('api/v1/', include('installations.urls')),
    path('', include('installations.urls')), # Test URL for installations
    path('', home),  # Test URL for home
]
#path('', include('api.urls', namespace='api'))