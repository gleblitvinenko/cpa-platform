from django.contrib.auth import get_user_model
from rest_framework import serializers

from offer.models import Offer
from user.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=get_user_model().USER_TYPE_CHOICES)

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "password", "is_staff", "user_type")
        read_only_fields = ("is_staff",)
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, set the password correctly and return it"""
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()

        return user


class UserBrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "is_staff", "user_type", "telegram_username", "brand_name", "offers", "minimal_withdraw", "phone_number", "balance")
        read_only_fields = ("is_staff", "user_type", "minimal_withdraw", "email", "offers", "balance")


class UserInfluencerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("id", "email", "is_staff", "user_type", "telegram_username", "offers", "minimal_withdraw", "phone_number", "balance")
        read_only_fields = ("is_staff", "user_type", "minimal_withdraw", "email", "offers", "balance", "brand_name")


class UserForAdminsSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"
