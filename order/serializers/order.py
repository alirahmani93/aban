from decimal import Decimal

from rest_framework import serializers

from order.models.currency import CurrencyCodes, Currency
from order.services.order import OrderServiceInterface


class OrderSerializer(serializers.Serializer):
    currency_code = serializers.ChoiceField(choices=CurrencyCodes.choices)
    amount = serializers.DecimalField(min_value=Decimal(0), max_digits=18, decimal_places=10)

    def create(self, validated_data):
        currency = Currency.objects.get(code=validated_data['currency_code'])
        service = OrderServiceInterface(
            user=self.context.get('request').get('user'),
            currency=currency,
            amount=validated_data['amount'],
            price=Decimal(4),
        )
        return service.create_order_manager()
