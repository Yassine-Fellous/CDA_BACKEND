from .views import register_view
from .views import login_view
from django.urls import path
from .views import verify_code_view
from .views import request_password_reset
from .views import reset_password
from .views import health_check


urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('verify/', verify_code_view, name='verify'),
    path('request-password-reset/', request_password_reset, name='request-password-reset'),
    path('reset-password/', reset_password, name='reset-password'),
    path('health/', health_check, name='health_check'),
]