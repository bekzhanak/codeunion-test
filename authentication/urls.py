from django.urls import path
from .views import RegisterUserAPIView
from rest_framework.authtoken import views

urlpatterns = [
    path("register/", RegisterUserAPIView.as_view(), name="register"),
    path("api-token-auth/", views.obtain_auth_token, name="obtain_token")
]
