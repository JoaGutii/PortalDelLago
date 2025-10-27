from django.urls import path
from .views import RegisterView, login_view, password_reset_request

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
    path('password-reset/', password_reset_request, name='password-reset'),
]
