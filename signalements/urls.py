from django.urls import path
from . import views

urlpatterns = [
    # Route utilisateur standard
    path('create/', views.create_signalement, name='create_signalement'),
    
    # Routes d'administration (sans api/v1)
    path('admin/list/', views.admin_list_signalements, name='admin_list_signalements'),
    path('admin/<int:signalement_id>/update/', views.admin_update_signalement, name='admin_update_signalement'),
    path('admin/<int:signalement_id>/delete/', views.admin_delete_signalement, name='admin_delete_signalement'),
    path('admin/stats/', views.admin_stats_signalements, name='admin_stats_signalements'),
    path('admin/utilisateurs/', views.admin_list_utilisateurs, name='admin_list_utilisateurs'),
]