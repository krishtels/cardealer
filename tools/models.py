from datetime import date

from django.core.serializers.json import DjangoJSONEncoder
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)
    updated = models.DateField(auto_now=True)
    created = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True


class Sale(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    amount_to_get_sale = models.IntegerField(default=0)
    percent = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0.00), MaxValueValidator(100.00)],
        default=0.0,
    )
    params = models.JSONField(encoder=DjangoJSONEncoder, null=True)

    date_start = models.DateField(default=date.today)
    date_end = models.DateField(default=date_start)

    class Meta:
        abstract = True
