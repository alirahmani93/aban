from django.db import models


class CurrencyCodes(models.TextChoices):
    IRT = "irt", "Irt"
    ABAN = "aban", "Aban"


class OrderStates(models.IntegerChoices):
    INIT = 0, 'Init'
    SUCCEED = 1, 'Succeed'
    WAIT_FOR_PARTIAL = 2, 'Wait For Partial'
