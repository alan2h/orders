from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    stock = serializers.IntegerField(min_value=1)

    class Meta:
        model = Product
        fields = ['name', 'price', 'stock']
