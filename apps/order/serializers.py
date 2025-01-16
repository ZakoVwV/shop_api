from rest_framework import serializers

from apps.order.models import Order, OrderItem

from apps.product.models import Product


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'product_title']


class OrderSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)
    user = serializers.ReadOnlyField(source='users.email')
    products = OrderItemSerializer(write_only=True, many=True)
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        products = validated_data['products']
        user = self.context['request'].user

        total_sum = sum(product['quantity'] * product['product'].price for product in products)

        order = Order.objects.create(user=user, status='open', total_sum=total_sum)

        order_item_objects = [
            OrderItem(order=order,
                      product=product['product'],
                      quantity=product['quantity']) for product in products
        ]

        OrderItem.objects.bulk_create(order_item_objects)
        return order

    def get_order_items(self, instance):
        return OrderItemSerializer(instance.items.all(), many=True).data