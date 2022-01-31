from django.db import models

from ..products.models import Product

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


class OrderDetail(models.Model):

    order = models.ForeignKey(Order, related_name='details',
                              on_delete=models.PROTECT)
    cuantity = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
