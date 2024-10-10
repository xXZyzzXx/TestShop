from typing import TypedDict

from rest_framework import serializers

from apps.catalog.models import Product
from apps.catalog.serializers import ProductSerializer
from apps.orders.models import Order, OrderItem, Reservation


class OrderItemCreateSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product"
    )
    quantity = serializers.IntegerField(min_value=1)


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ["product", "quantity", "price"]


class OrderItemData(TypedDict):  # TODO: should be renamed to avoid Data in title
    product: Product
    quantity: int


class OrderCreateSerializer(serializers.Serializer):
    items = OrderItemCreateSerializer(many=True)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["total_price", "created_at", "updated_at"]


class ReservationSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = Reservation
        fields = "__all__"
