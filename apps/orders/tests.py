
from rest_framework.test import APITestCase
from rest_framework import status


from django.contrib.auth.models import User


from ..products.models import Product


class OrderCase(APITestCase):

    def setUp(self):

        user = User.objects.create_user(username='admin',
                                        email='user@foo.com',
                                        password='se242403german')
        user.is_active = True
        user.save()

        Product.objects.create(
            name='example 1',
            price=27,
            stock=10
        )
        Product.objects.create(
            name='example 2',
            price=57,
            stock=5
        )

    def test_register_confirm(self):
        """
            confirm order,
            register order
        """

        user = User.objects.get(pk=1)
        self.client.force_authenticate(user=user)

        response = self.client.post(
            '/orders/api/',
            {'date_time': '2009-09-09', 'order_detail': [{
                    "cuantity": 5,
                    "product": 1
                    }, {
                        "cuantity": 5,
                        "product": 2
                    }]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_stock(self):
        """
            error order stock
        """

        user = User.objects.get(pk=1)
        self.client.force_authenticate(user=user)

        response = self.client.post(
            '/orders/api/',
            {'date_time': '2009-09-09', 'order_detail': [{
                "cuantity": 5,
                "product": 2
                }, {
                "cuantity": 5,
                "product": 3000
                }]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_repeat(self):
        """
            if product is repeat
        """

        user = User.objects.get(pk=1)
        self.client.force_authenticate(user=user)

        response = self.client.post(
            '/orders/api/',
            {'date_time': '2009-09-09', 'order_detail': [{
                    "cuantity": 5,
                    "product": 1
                    }, {
                        "cuantity": 5,
                        "product": 1
                    }]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
