from decimal import Decimal

from django.conf import settings
from django.db import models
from django.db.models import Sum

from apps.catalog.models import Product
from apps.utils.models import TimeStampModel, UUIDModel


class Order(UUIDModel, TimeStampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # statuses, is_paid, etc

    @property
    def total_price(self) -> Decimal:
        return self.items.aggregate(total=Sum("price"))["total"] or Decimal("0.00")

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="order_items", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Reservation(UUIDModel, TimeStampModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name="reservations", on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Reservation of {self.product.name} by {self.user.username}"
