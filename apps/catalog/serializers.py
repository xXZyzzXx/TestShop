from decimal import Decimal
from typing import Any, Dict, Optional, TypedDict

from django.db import transaction
from rest_framework import serializers

from apps.catalog.models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    parent_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source="parent",
        write_only=True,
        required=False,
    )
    parent = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    discounted_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ["available_stock"]

    def create(self, validated_data: Dict[str, Any]) -> Product:
        from apps.catalog.services import ProductService

        return ProductService.create_product(product_data=validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        # TODO: move entirely to service layer
        from apps.catalog.services import ProductService

        if "stock" in validated_data:
            ProductService.update_stock(
                product=instance, new_stock=validated_data.pop("stock")
            )
        return super().update(instance, validated_data)


class ProductCreateData(TypedDict):
    name: str
    description: Optional[str]
    price: Decimal
    discount_percentage: Decimal
    stock: int
    category: Category
    available_stock: int


class PriceUpdateSerializer(serializers.Serializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class PromotionStartSerializer(serializers.Serializer):
    discount_percentage = serializers.DecimalField(max_digits=5, decimal_places=2)
