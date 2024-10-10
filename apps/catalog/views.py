from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.catalog.models import Product
from apps.catalog.serializers import (
    PriceUpdateSerializer,
    ProductSerializer,
    PromotionStartSerializer,
)
from apps.catalog.services import ProductService


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(available_stock__gt=0)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = [
        "category__id",
    ]
    search_fields = ["name", "description"]
    ordering_fields = ["price", "name"]

    @extend_schema(request=PriceUpdateSerializer, responses={200: ProductSerializer})
    @action(detail=True, methods=["PATCH"], permission_classes=[IsAuthenticated])
    def change_price(self, request: Request, *args, **kwargs) -> Response:
        serializer = PriceUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_product: Product = ProductService.update_price(
            product=self.get_object(), new_price=serializer.validated_data["price"]
        )
        response_serializer = self.get_serializer(updated_product)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    @extend_schema(request=PromotionStartSerializer, responses={200: ProductSerializer})
    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def start_promotion(self, request: Request, *args, **kwargs) -> Response:
        serializer = PromotionStartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        updated_product: Product = ProductService.start_promotion(
            product=self.get_object(),
            discount_percentage=serializer.validated_data["discount_percentage"],
        )
        response_serializer = self.get_serializer(updated_product)
        return Response(response_serializer.data, status=status.HTTP_200_OK)
