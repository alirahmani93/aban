from decimal import Decimal

from django.db import models


class CurrencyDecimalField(models.DecimalField):
    INTEGER_PLACES = 15
    DECIMAL_PLACES = 7

    MAX_DIGITS = INTEGER_PLACES + DECIMAL_PLACES

    MAX_VALUE = Decimal("999999999999999.9999999")
    MIN_VALUE = Decimal("-999999999999999.9999999")

    def __init__(
            self,
            verbose_name=None,
            name=None,
            max_digits=MAX_DIGITS,
            decimal_places=DECIMAL_PLACES,
            **kwargs,
    ):
        super().__init__(
            verbose_name=verbose_name,
            name=name,
            max_digits=max_digits,
            decimal_places=decimal_places,
            **kwargs,
        )
