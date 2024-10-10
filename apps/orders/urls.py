from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.orders.views import OrderViewSet, ReservationViewSet

router = DefaultRouter()
router.register(r"reservations", ReservationViewSet, basename="reservation")
router.register(r"orders", OrderViewSet, basename="orders")

urlpatterns = [
    path("", include(router.urls)),
]
