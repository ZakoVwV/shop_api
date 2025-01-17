from rest_framework import serializers

from .models import Product, ProductImage

from apps.review.serializers import CommentSerializer

from django.db.models import Avg

class ProductBaseSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    def get_discounted_price(self, instance):
        if instance.discount is not None:
            discounted_price = instance.price - (instance.price * instance.discount / 100)
            return discounted_price
        return None

    def get_average_rating(self, instance):
        return instance.reviews.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0.0


class ProductListSerializer(ProductBaseSerializer):
    discounted_price = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'stock', 'discounted_price', 'average_rating']


class ProductDetailSerializer(ProductBaseSerializer):
    discounted_price = serializers.SerializerMethodField()
    owner = serializers.ReadOnlyField(source='owner.email')
    product_images = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_product_images(self, instance):
        product_images = instance.images.all()
        if product_images:
            return ProductImageSerializer(product_images, many=True).data
        return None

    def get_comment(self, instance):
        comments = instance.comments.all()
        if comments:
            return CommentSerializer(comments, many=True).data
        else:
            return None



class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'title',
            'price',
            'description',
            'quantity',
            'discount',
            'category'
        ]


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = '__all__'


class ProductUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'





