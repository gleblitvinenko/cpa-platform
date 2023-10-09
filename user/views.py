from django.contrib.auth import get_user_model
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.permissions import AllowUnauthenticatedOnly, IsAdministratorUser
from user.serializers import UserSerializer, UserBrandSerializer, UserInfluencerSerializer, UserForAdminsSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = (AllowUnauthenticatedOnly,)


class MyProfileView(generics.RetrieveUpdateAPIView):
    queryset = get_user_model().objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        instance = self.get_object()
        if instance.user_type == 'brand':
            return UserBrandSerializer
        else:
            return UserInfluencerSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserForAdminsSerializer
    permission_classes = (IsAdministratorUser,)
