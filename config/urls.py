# Copyright (c) 2025
# Yassine Fellous, Abdelkader Sofiane Ziri, Mathieu Duverne, Mohamed Marwane Bellagha
# Tous droits réservés. Utilisation interdite sans autorisation écrite des auteurs.

from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

#lien vers les vues de l'application installations
#qui affichent les données des installations sportives
#pour les tests de l'API
from installations import views
def home(request):
    html = """
    <h1>Bienvenue sur l'API CDA Backend !</h1>
    <ul>
        <li><a href="/api/v1/sports/">/api/v1/sports/</a></li>
        <li><a href="/api/v1/equipments/">/api/v1/equipments/</a></li>
        <li><a href="/api/v1/geojson/">/api/v1/geojson/</a></li>
        <li><a href="/api/v1/installations/">/api/v1/installations/</a></li>
    </ul>
    <p>URL de base : <b>https://cdabackend-production.up.railway.app</b></p>
    """
    return HttpResponse(html)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('installations.urls')),
    #path('', include('installations.urls')), # Test URL for installations
    path('', home),  # Test URL for home
]
#path('', include('api.urls', namespace='api'))