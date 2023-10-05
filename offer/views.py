from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from offer.models import Offer, Category
from offer.serializers import OfferListSerializer, OfferDetailSerializer, OfferCreateSerializer, CategorySerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return OfferListSerializer
        if self.action == "create":
            return OfferCreateSerializer
        return OfferDetailSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Offer.objects.all().filter(is_active=True)
        return Offer.objects.all()


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)
