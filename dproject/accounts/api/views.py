from rest_framework import generics
from .serializers import (
    UserRegistrationSerializer,
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
    UserSerializer,
)
from accounts.models import User, UserProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
import re


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, id=None):
        if id:
            try:
                user = User.objects.get(id=id)
            except User.DoesNotExist:
                return Response({'detail': 'User not found'}, status=404)
        else:
            user = request.user

        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, id=None):
        if id and id != request.user.id:
            return Response({'detail': 'Permission denied'}, status=403)

        user = request.user

        phone = request.data.get('phone')
        if phone and not re.fullmatch(r'01[0-9]{9}', phone):
            return Response({'phone': 'Phone number must be a valid Egyptian number (starts with 01 and 11 digits).'}, status=400)

        user.first_name = request.data.get('first_name', user.first_name)
        user.last_name = request.data.get('last_name', user.last_name)
        user.username = request.data.get('username', user.username)
        user.phone = phone or user.phone
        user.save()

        profile = user.profile
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserSerializer(user).data) 
        return Response(serializer.errors, status=400)