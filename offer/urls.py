from django.urls import path, include
from rest_framework import routers

from offer.views import OfferViewSet

router = routers.DefaultRouter()
router.register('', OfferViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = 'offer'
