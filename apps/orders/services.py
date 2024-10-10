from decimal import Decimal
from typing import List

from django.contrib.auth.models import User
from django.db import transaction

from apps.catalog.models import Product
from apps.catalog.services import ProductService
from apps.orders.exceptions import InsufficientStock
from apps.orders.models import Order, OrderItem, Reservation
from apps.orders.serializers import OrderItemData


class OrderService:

    @classmethod
    @transaction.atomic
    def create_order(cls, user: User, items_data: List[OrderItemData]) -> Order:
        """Create a new order and update products available stock"""
        order: Order = Order.objects.create(user=user)
        for item_data in items_data:
            product: Product = item_data["product"]
            quantity: int = item_data["quantity"]
            if product.available_stock < quantity:
                raise InsufficientStock(
                    f"{InsufficientStock.default_detail} for product {product.name}"
                )

            ProductService.update_stock(
                product=product, new_stock=product.stock - quantity
            )
            price: Decimal = product.discounted_price * quantity
            OrderItem.objects.create(
                order=order, product=product, quantity=quantity, price=price
            )
        return order

    #  def update_order, etc


class ReservationService:

    @classmethod
    @transaction.atomic
    def create_reservation(
        cls,
        product: Product,
        quantity: int,
        user: User,
    ) -> Reservation:
        if product.available_stock < quantity:
            raise InsufficientStock("Not enough available stock to reserve")

        ProductService.update_stock(product=product, new_stock=product.stock - quantity)
        reservation = Reservation.objects.create(
            user=user, product=product, quantity=quantity
        )
        return reservation

    @classmethod
    @transaction.atomic
    def cancel_reservation(cls, reservation: Reservation) -> None:
        product: Product = reservation.product

        ProductService.update_stock(
            product=product, new_stock=product.stock + reservation.quantity
        )
        reservation.delete()
