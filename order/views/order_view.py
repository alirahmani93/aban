
from rest_framework.permissions import IsAuthenticated

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from order.models.order import Order

from order.serializers.order import OrderSerializer


class OrderViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.is_available()
    permission_classes = [IsAuthenticated]

