from django.db import models

from ..products.models import Product
from .services import DolarsiService
from ..libs.models import ClicOh


class Order(ClicOh):

    date_time = models.DateTimeField()

    @property
    def get_total(self):
        """Get total method.

        Calculate the total price of the order.
        """
        details = OrderDetail.objects.filter(order__id=self.id)
        return sum([i.product.price * i.cuantity for i in details])

    @property
    def get_total_usd(self):
        """Get total in usd method.

        Calculate the total price of the order and convert in service.
        """
        dolar_service = DolarsiService()
        details = OrderDetail.objects.filter(order__id=self.id)
        amount = sum([i.product.price * i.cuantity for i in details])
        return dolar_service.convert(amount)


class OrderDetail(models.Model):

    order = models.ForeignKey(Order, related_name='details',
                              on_delete=models.PROTECT)
    cuantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
