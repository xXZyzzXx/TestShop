from django.contrib import admin

from apps.orders.models import Order, OrderItem, Reservation


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product", "quantity", "created_at")
    list_filter = ("created_at", "product")
    search_fields = ("user__username", "product__name")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "total_price", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("user__username",)
    inlines = [OrderItemInline]

    @staticmethod
    def total_price(obj):
        return obj.total_price
