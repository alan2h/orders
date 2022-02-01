

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .serializers import OrderSerializer, OrderListSerializer
from .models import Order
from .repositories import OrderRepository


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    queryset = Order.objects.filter(remove=False)
    serializer_class = OrderSerializer
    serializer_class_listing = OrderListSerializer
    permission_classes = [IsAuthenticated]
    order_repository = OrderRepository()

    def perform_destroy(self, instance):
        self.order_repository.restore_stock(instance.id)
        instance.remove = True
        instance.save()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = self.order_repository.create_order(**serializer.data)
        return Response({"status": 'created', "data": data},
                        status=201)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class_listing(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class_listing(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.serializer_class(data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.order_repository.update_order(self.get_object(),
                                           **serializer.data)
        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}
        return Response({"status": 'updated', "data": serializer.data},
                        status=200)
