
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import ProductSerializer
from .models import Product


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.filter(remove=False)
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        instance.remove = True
        instance.save()
