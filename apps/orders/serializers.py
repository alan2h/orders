
from apps.products.serializers import ProductSerializer
from rest_framework import serializers

from ..products.models import Product
from .models import Order, OrderDetail


class OrderDetailSerializer(serializers.ModelSerializer):

    cuantity = serializers.IntegerField()
    product = serializers.IntegerField()

    def validate(self, data):

        if Product.objects.filter(id=data['product'], remove=False).exists():
            product_object = Product.objects.get(pk=data['product'])
            if product_object.stock < data['cuantity']:
                raise serializers.ValidationError(
                    'quantity is greater than stock')
            return data
        raise serializers.ValidationError('this product not exists.')

    class Meta:
        model = OrderDetail
        fields = ['cuantity', 'product']


class OrderSerializer(serializers.ModelSerializer):

    date_time = serializers.DateTimeField()
    order_detail = serializers.JSONField()
    details = OrderDetailSerializer(many=True, required=False)

    def validate_order_detail(self, value):
        """
         check if orderDetail
        """
        for i in range(0, len(value)):
            for j in range(i+1, len(value)):
                if(value[i]['product'] == value[j]['product']):
                    raise serializers.ValidationError(
                        'this product is duplicated')
        serializer = OrderDetailSerializer(data=value, many=True)
        if serializer.is_valid():
            return value
        else:
            raise serializers.ValidationError(serializer.errors)

    class Meta:
        model = Order
        fields = (
            'id',
            'date_time',
            'details',
            'get_total',
            'order_detail'
        )
