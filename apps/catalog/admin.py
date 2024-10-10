from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from apps.catalog.models import Category, Product


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ("tree_actions", "indented_title", "id", "name", "parent")
    list_display_links = ("indented_title",)
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "id", "category", "price", "stock", "available_stock")
    list_filter = ("category",)
    search_fields = ("name", "description")
    readonly_fields = ("available_stock",)
