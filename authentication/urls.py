from .views import register_view
from django.urls import path


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
]