from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from apps.utils.models import TimeStampModel, UUIDModel


class Category(MPTTModel, UUIDModel, TimeStampModel):
    name = models.CharField(max_length=255, db_index=True)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ("parent", "name")

    def __str__(self):
        return self.name


class Product(UUIDModel, TimeStampModel):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=0.0
    )
    stock = models.PositiveIntegerField(default=0)
    available_stock = models.PositiveIntegerField(default=0)
    category = TreeForeignKey(
        Category, related_name="products", on_delete=models.CASCADE
    )

    @property
    def discounted_price(self):
        if self.discount_percentage > 0:
            return self.price * (1 - self.discount_percentage / 100)
        return self.price

    def __str__(self):
        return self.name
