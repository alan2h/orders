
from rest_framework.test import APITestCase
from rest_framework import status


from django.contrib.auth.models import User


class ProductCase(APITestCase):

    def setUp(self):

        user = User.objects.create_user(username='admin',
                                        email='user@foo.com',
                                        password='se242403german')
        user.is_active = True
        user.save()

    def test_register_confirm(self):
        """
            confirm product,
            register product
        """

        user = User.objects.get(pk=1)
        self.client.force_authenticate(user=user)

        response = self.client.post(
            '/products/api/',
            {
                'name': 'example',
                'price': 23.3,
                'stock': 2,
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_product_stock(self):
        """
            error product repeat
        """

        user = User.objects.get(pk=1)
        self.client.force_authenticate(user=user)

        response = self.client.post(
            '/products/api/',
            {
                'name': 'example',
                'price': 23.3,
                'stock': -2,
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
