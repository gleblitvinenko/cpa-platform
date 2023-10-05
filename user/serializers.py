from django.contrib.auth import get_user_model
from rest_framework import serializers

from offer.models import Offer
from user.models import Brand, Influencer, CustomUser


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=get_user_model().USER_TYPE_CHOICES)

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff", "user_type")
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}, "user_type": {"write_only": True}}

    def create(self, validated_data):
        user_type = validated_data.pop("user_type", None)

        if user_type not in dict(get_user_model().USER_TYPE_CHOICES):
            raise serializers.ValidationError("Invalid user_type.")

        user = get_user_model().objects.create_user(**validated_data, user_type=user_type)

        if user_type == 'brand':
            Brand.objects.create(user=user, brand_name=None)
        elif user_type == 'influencer':
            Influencer.objects.create(user=user, telegram_username=None)

        return user

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class BrandProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    offers = OfferSerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = ('user', 'brand_name', 'minimum_cabinet_price', 'offers')


class InfluencerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    offers = OfferSerializer(many=True, read_only=True)

    class Meta:
        model = Influencer
        fields = ('user', 'telegram_username', 'minimum_cabinet_price', 'offers')


class ProfileSerializer(serializers.Serializer):
    brand = BrandProfileSerializer()
    influencer = InfluencerProfileSerializer

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff", "user_type", "brand", "influencer")
