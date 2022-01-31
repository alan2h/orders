from unicodedata import decimal
from django.db import models


from ..libs.models import ClicOh


class Product(ClicOh):

    name = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.IntegerField(default=1)
