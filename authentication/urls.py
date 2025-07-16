from .views import register_view
from .views import login_view
from django.urls import path
from .views import verify_code_view


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('verify/', verify_code_view, name='verify'),
]