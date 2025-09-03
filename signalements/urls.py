from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_signalement, name='create_signalement'),
    path('', views.list_signalements, name='list_signalements'),  # Optionnel
]