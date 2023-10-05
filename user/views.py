from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.serializers import UserSerializer, ProfileSerializer, OfferSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class MyProfileView(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    @action(detail=True, methods=['post'], url_name="add-offer")
    def create_offer(self, request):
        user = self.get_object()
        user_type = user.user_type

        if user_type == 'brand':
            brand = user.brand
            data = request.data
            data['brand'] = brand.id  # Associate the offer with the brand
            serializer = OfferSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({'detail': 'Offers can only be added by Brand users.'}, status=status.HTTP_403_FORBIDDEN)