
from django.db import transaction

from .models import Order, OrderDetail
from ..products.models import Product


class OrderRepository:

    @transaction.atomic
    def create_order(self, **param):
        """
            create an order with your details
        """
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
        """
            rest in stock quantity
        """
        product = Product.objects.get(pk=product_id)
        product.stock -= cuantity
        product.save()

    def add_stock(self, product_id, cuantity):
        """
            add a quantity to stock
        """
        product = Product.objects.get(pk=product_id)
        product.stock += cuantity
        product.save()

    def restore_stock(self, order_id):
        """
            restore quantity when an order is canceled
        """
        order_details = OrderDetail.objects.filter(order=order_id)
        for detail in order_details:
            self.add_stock(detail.product.id, detail.cuantity)

    @transaction.atomic
    def update_order(self, order, **param):

        """
          update order,
          when product is the same, restore or substrac stock
          when product is'nt same, restore old stock product
        """

        order_details = OrderDetail.objects.filter(order=order.id)
        order.date_time = param['date_time']
        order.save()
        count = 0
        for detail in order_details:
            cuantity = param['order_detail'][count]['cuantity']
            product_id = param['order_detail'][count]['product']

            if (cuantity < detail.cuantity) \
                    and detail.product.id == product_id:
                result = detail.cuantity - cuantity
                self.add_stock(detail.product.id, result)

            if (cuantity > detail.cuantity) \
                    and detail.product.id == product_id:
                result = cuantity - detail.cuantity
                self.subtract_stock(detail.product.id, result)

            if detail.product.id != product_id:
                self.add_stock(detail.product.id, detail.cuantity)

            detail.product = Product.objects.get(pk=product_id)
            detail.cuantity = cuantity
            detail.save()
            count += 1
