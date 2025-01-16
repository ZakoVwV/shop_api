from django.db import models

from apps.product.models import Product

from django.contrib.auth import get_user_model


class OrderItem(models.Model):
    order = models.ForeignKey(
        'Order',
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='items'
    )
    quantity = models.IntegerField(default=1)

User = get_user_model()

class Order(models.Model):
    STATUS_CHOICES = (
        ('open', 'Открыт'),
        ('in_process', 'В обработке'),
        ('closed', 'Завершен')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    product = models.ManyToManyField(Product, through=OrderItem)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    total_sum = models.DecimalField(max_digits=9, decimal_places=2, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

