
from rest_framework import viewsets


from .serializers import ProductSerializer
from .models import Product


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.filter(remove=False)
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        instance.remove = True
        instance.save()

