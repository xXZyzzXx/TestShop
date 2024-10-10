from decimal import Decimal

from apps.catalog.models import Product
from apps.catalog.serializers import ProductCreateData


class ProductService:
    """Repository for Product-related operations"""

    @classmethod
    def create_product(
        cls,
        product_data: ProductCreateData,  # TODO: should be renamed to avoid Data in title
    ) -> Product:
        product_data["available_stock"] = product_data.get("stock")
        return Product.objects.create(**product_data)

    @classmethod
    def update_price(cls, product: Product, new_price: Decimal) -> Product:
        product.price = new_price
        product.save(update_fields=["price"])
        return product

    @classmethod
    def update_stock(cls, product: Product, new_stock: int) -> Product:
        """Update the stock and available stock of a product"""
        delta = new_stock - product.stock
        product.stock = new_stock
        product.available_stock += delta
        if product.available_stock < 0:
            product.available_stock = 0
        product.save(update_fields=["stock", "available_stock"])
        return product

    @classmethod
    def start_promotion(cls, product: Product, discount_percentage: Decimal) -> Product:
        """Start a promotion by setting a discount"""
        product.discount_percentage = discount_percentage
        product.save(update_fields=["discount_percentage"])
        return product
