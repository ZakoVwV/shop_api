from django.urls import path

from apps.order.views import OrderListCreateView

urlpatterns = [
    path('order-create/', OrderListCreateView.as_view())
]