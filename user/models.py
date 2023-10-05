from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.db import models


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(null=True, max_length=15, validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Phone number  must be entered in the format: '+999999999'. Up to 15 digits allowed."
        )
    ])
    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    USER_TYPE_CHOICES = (
        ('brand', 'Brand'),
        ('influencer', 'Influencer'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


class Brand(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    brand_name = models.CharField(max_length=255, null=True)
    minimum_cabinet_price = models.DecimalField(max_digits=7, decimal_places=2, default=10000.00)


class Influencer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    telegram_username = models.CharField(max_length=55, null=True)
    offers = models.ManyToManyField("offer.Offer", related_name='influencers')
    minimum_withdrawal_amount = models.DecimalField(max_digits=7, decimal_places=2, default=1000.00)


class InfluencerOffer(models.Model):
    influencer = models.ForeignKey(Influencer, on_delete=models.CASCADE)
    offer = models.ForeignKey("offer.Offer", on_delete=models.CASCADE)
    generated_link = models.URLField()
    taken_date = models.DateTimeField(auto_now_add=True)
