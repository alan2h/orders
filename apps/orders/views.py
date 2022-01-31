

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import OrderSerializer
from .models import Order
from .repositories import OrderRepository


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    queryset = Order.objects.filter(remove=False)
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_destroy(self, instance):
        order_repository = OrderRepository()
        order_repository.restore_stock(instance.id)
        instance.remove = True
        instance.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_repository = OrderRepository()
        data = order_repository.create_order(**serializer.data)
        return Response({"status": 'created', "data": data},
                        status=201)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)
