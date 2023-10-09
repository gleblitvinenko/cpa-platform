import random
import string

from rest_framework import serializers

from offer import models
from offer.models import Category, Offer
from user.models import CustomUserOffer


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
        fields = ('id', 'title', 'is_active', 'description', 'category', 'payout', 'price', 'creation_date', "is_vip")
        read_only_fields = ('is_active',)


class OfferCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = models.Offer
        fields = ('title', 'description', 'is_active', 'category', 'payout', 'price')
        read_only_fields = ('is_active',)


class OfferAdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Offer
        fields = "__all__"


class CustomUserOfferSerializer(serializers.ModelSerializer):
    # Удаляем generated_link из полей сериализатора

    class Meta:
        model = CustomUserOffer
        fields = ("id", "user", "offer")

    def create(self, validated_data):
        user = validated_data['user']
        offer = validated_data['offer']

        # Генерируем случайную строку длиной 10 символов для generated_link
        generated_link = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

        custom_user_offer = CustomUserOffer.objects.create(
            user=user,
            offer=offer,
            generated_link=generated_link,
        )

        return custom_user_offer
