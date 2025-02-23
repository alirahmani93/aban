from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models

from utilities import BaseModel
from utilities.fields.decimal import CurrencyDecimalField


class Wallet(BaseModel):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    currency = models.ForeignKey('order.Currency', on_delete=models.PROTECT)

    balance = CurrencyDecimalField(default=Decimal(0))
    freeze = CurrencyDecimalField(default=Decimal(0))

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'currency'],
                name="wallet_unique_user_currency"
            )
        ]
