import uuid

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from offer.models import Offer, Category
from offer.permissions import IsAdminOrBrandUser, IsInfluencer
from offer.serializers import OfferListSerializer, OfferDetailSerializer, OfferCreateSerializer, CategorySerializer, \
    OfferAdminSerializer, CustomUserOfferSerializer


class OfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    permission_classes = (IsAuthenticated, IsAdminOrBrandUser)

    def get_serializer_class(self):
        if self.action == 'list':
            return OfferListSerializer
        if self.action == "create":
            return OfferCreateSerializer
        if self.action == "add_to_my_offers":
            return CustomUserOfferSerializer
        return OfferDetailSerializer

    def get_queryset(self):
        if not self.request.user.is_staff:
            return Offer.objects.all().filter(is_active=True)
        return Offer.objects.all()

    @action(detail=True, methods=['post'], url_path='add_to_my_offers', permission_classes=[IsInfluencer])
    def add_to_my_offers(self, request, pk=None):
        # Получаем оффер по его идентификатору (pk)
        offer = self.get_object()

        # Проверка, что оффер активен
        if not offer.is_active:
            return Response({'error': 'The offer is not active.'}, status=status.HTTP_400_BAD_REQUEST)

        # Получаем текущего авторизованного пользователя из запроса
        user = request.user

        # Используем pk из URL как offer_id
        offer_id = pk

        # Генерируем уникальный URL для оффера
        generated_url = str(uuid.uuid4())[:12]  # Пример: '6fd2a8b1-7a8b'

        # Создаем данные для сериализатора
        data = {
            'user': user.id,
            'offer': offer_id,
            'generated_link': generated_url,  # Устанавливаем сгенерированный URL
        }

        serializer = CustomUserOfferSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminOfferViewSet(viewsets.ModelViewSet):
    queryset = Offer.objects.all()
    serializer_class = OfferAdminSerializer
    permission_classes = (IsAdminUser,)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUser,)
