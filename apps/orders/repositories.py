
from django.db import transaction

from .models import Order, OrderDetail
from ..products.models import Product


class OrderRepository:

    @transaction.atomic
    def create_order(self, **param):
        order = Order.objects.create(date_time=param['date_time'])
        for detail in param['order_detail']:
            self.subtract_stock(detail['product'], detail['cuantity'])
            OrderDetail.objects.create(
                order=order,
                product=Product.objects.get(pk=detail['product']),
                cuantity=detail['cuantity']
            )
        return param

    def subtract_stock(self, product_id, cuantity):

        product = Product.objects.get(pk=product_id)
        product.stock -= cuantity
        product.save()

    def restore_stock(self, order_id):
        order_details = OrderDetail.objects.filter(order=order_id)
        for detail in order_details:
            product = Product.objects.get(pk=detail.product.id)
            product.stock += detail.cuantity
            product.save()


