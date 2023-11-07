from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer
from rest_framework import generics


# Class based view to register user
class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer
