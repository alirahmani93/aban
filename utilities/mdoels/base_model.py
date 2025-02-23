import abc

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('زمان ایجاد'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('زمان به روزرسانی'))

    class Meta:
        abstract = True
