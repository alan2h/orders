
from rest_framework.test import APITestCase
from rest_framework import status
from unittest import mock


from django.contrib.auth.models import User


from ..products.models import Product


class OrderCase(APITestCase):

    def setUp(self):

        user = User.objects.create_user(username='admin',
                                        email='user@foo.com',
                                        password='se242403german',
                                        is_active=True)
        self.user = user

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

    @mock.patch('apps.orders.services.DolarsiService.convert')
    def test_register_confirm(self, mock_dolar):
        """
            confirm order,
            register order
        """

        self.client.force_authenticate(user=self.user)

        mock_response = mock.Mock()
        mock_response.status_code = 201
        mock_dolar.return_value = '204.4'

        response = self.client.post(
            '/orders/api/',
            {'date_time': '2009-09-09', 'order_detail': [{
                    "cuantity": 5,
                    "product": 1
                    }]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_stock(self):
        """
            error order stock
        """

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            '/orders/api/',
            {'date_time': '2009-09-09', 'order_detail': [{
                "cuantity": 5,
                "product": 2
                }, {
                "cuantity": 3000,
                "product": 5
                }]},
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_product_repeat(self):
        """
            if product is repeat
        """

        self.client.force_authenticate(user=self.user)

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
