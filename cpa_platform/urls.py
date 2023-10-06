"""
URL configuration for cpa_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from offer.views import CategoryViewSet, AdminOfferViewSet

router_categories = routers.DefaultRouter()
router_categories.register('', CategoryViewSet, basename="category")

router_admin_offers = routers.DefaultRouter()
router_admin_offers.register("", AdminOfferViewSet, basename="admin_offer")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/offers/', include('offer.urls', namespace='offer')),
    path('api/users/', include('user.urls', namespace='user')),
    path("api/categories/", include(router_categories.urls)),
    path("api/admin_offers/", include(router_admin_offers.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path("__debug__/", include("debug_toolbar.urls")),

]
