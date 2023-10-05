from django.db import models

from user.models import Brand


class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return f"{self.title}"


class Offer(models.Model):

    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    category = models.ForeignKey(Category, related_name="offer_category", on_delete=models.CASCADE)
    payout = models.DecimalField(max_digits=7, decimal_places=2)
    creation_date = models.DateTimeField(auto_now_add=True)
    brand = models.ForeignKey(Brand, related_name="offers", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title}"
