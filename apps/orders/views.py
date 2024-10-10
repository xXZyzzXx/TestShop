from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from apps.orders.models import Order, Reservation
from apps.orders.serializers import (
    OrderCreateSerializer,
    OrderSerializer,
    ReservationSerializer,
)
from apps.orders.services import OrderService, ReservationService


class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["POST"])
    def reserve(self, request: Request) -> Response:
        serializer = ReservationSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        reservation: Reservation = ReservationService.create_reservation(
            user=request.user,
            product=serializer.validated_data["product"],
            quantity=serializer.validated_data["quantity"],
        )

        response_serializer = ReservationSerializer(reservation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["POST"])
    def cancel(self, request: Request, *args, **kwargs) -> Response:
        ReservationService.cancel_reservation(
            reservation=self.get_object(),
        )
        return Response({"detail": "Reservation cancelled"}, status=status.HTTP_200_OK)

    # def delete, etc


class OrderViewSet(viewsets.ModelViewSet):  # Can be changed to Generic
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["items__product__id", "user__id", "sold_at"]
    search_fields = ["items__product__name"]
    ordering_fields = ["sold_at"]

    def create(self, request: Request, *args, **kwargs) -> Response:
        """Create a new Order and update the available stock of the Products"""
        serializer = OrderCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        order = OrderService.create_order(
            user=request.user, items_data=serializer.validated_data["items"]
        )
        response_serializer = self.get_serializer(order)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
