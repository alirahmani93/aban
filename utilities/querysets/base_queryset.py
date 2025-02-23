from django.db import models


class BaseQuerySet(models.QuerySet):
    def is_available(self):
        return self.filter(is_active=True)
