from django.contrib.auth.models import User
from django.db import models

from order.choices import OrderStates
from order.querysets.order_queryset import OrderQuerySet, OrderManager
from utilities import BaseModel
from utilities.fields.decimal import CurrencyDecimalField


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    currency = models.ForeignKey('order.Currency', on_delete=models.PROTECT)
    amount = CurrencyDecimalField()
    price = CurrencyDecimalField()
    total_price = CurrencyDecimalField()
    state = models.PositiveSmallIntegerField(choices=OrderStates.choices, default=OrderStates.INIT)
    is_partial = models.BooleanField()

    start_buying = models.DateTimeField(null=True, blank=True)
    pending_at = models.DateTimeField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)

    objects = OrderManager.from_queryset(OrderQuerySet)()

    def __str__(self):
        return f"{self.name} {self.price}"
