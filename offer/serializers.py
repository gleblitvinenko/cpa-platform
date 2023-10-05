from rest_framework import serializers

from offer import models
from offer.models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = ('title',)


class OfferListSerializer(serializers.ModelSerializer):

    category = serializers.StringRelatedField()

    class Meta:
        model = models.Offer
        fields = ('title', 'is_active', 'category', 'payout',)
        read_only_fields = ('is_active',)


class OfferDetailSerializer(OfferListSerializer):

    class Meta:
        model = models.Offer
        fields = ('id', 'title', 'is_active', 'description', 'category', 'payout', 'price', 'creation_date')  # TODO brand
        read_only_fields = ('is_active',)


class OfferCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = models.Offer
        fields = ('title', 'description', 'is_active', 'category', 'payout', 'price')
        read_only_fields = ('is_active',)
