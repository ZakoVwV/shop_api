from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

from apps.category.models import Category

User = get_user_model()


class Product(models.Model):
    STATUS_CHOICES = (
        ('in_stock', 'В наличий'),
        ('out_of_stock', 'Не в наличий')
    )

    title = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=0)
    description = models.TextField()
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True
    )
    stock = models.CharField(choices=STATUS_CHOICES, max_length=20, blank=True, null=True)
    discount = models.IntegerField(blank=True, null=True, validators=[
    MinValueValidator(0), MaxValueValidator(100)
    ])
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products'
    )

    def __str__(self):
        return f'{self.title} -> {self.quantity} -> {self.stock}'

    def save(self, *args, **kwargs):
        if self.quantity > 0:
            self.stock = 'in_stock'
        else:
            self.stock = 'out_of_stock'
        return super().save(*args, **kwargs)


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='product-images/')

    def __str__(self):
        return f'{self.product}'







