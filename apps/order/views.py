from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from apps.order.serializers import OrderSerializer
from apps.order.models import Order


class OrderListCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related(
            'items'
        )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=201)


