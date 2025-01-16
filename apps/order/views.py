from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response

from apps.order.serializers import OrderSerializer


class OrderListCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_orders = user.orders.all()
        serializer = self.serializer_class(user_orders, many=True)
        return Response(serializer.data, status=201)


