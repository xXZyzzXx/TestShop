from rest_framework import status
from rest_framework.exceptions import APIException


class InsufficientStock(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Not enough stock available"
    default_code = "insufficient_stock"


class ReservationNotFound(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = "Reservation not found or access denied"
    default_code = "reservation_not_found"
