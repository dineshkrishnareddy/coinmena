# -*- encoding: utf-8 -*-

from django.db import models


class Exchanges(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    from_currency = models.CharField(max_length=10)
    to_currency = models.CharField(max_length=10)
    value = models.FloatField()
