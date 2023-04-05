from django.core.validators import MinValueValidator
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
        validators=[MinValueValidator(0.00)],
        default=0.0,
    )

    date_start = models.DateField(auto_now_add=True)
    date_end = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True
