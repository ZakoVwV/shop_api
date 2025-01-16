from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination

from apps.generals.permissions import IsOwner, IsProductOwner
from apps.product.models import Product, ProductImage
from apps.product.seriallizers import ProductDetailSerializer, ProductListSerializer, ProductCreateSerializer, ProductImageSerializer, ProductUpdateSerializer

class StandardResultPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'page'


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    pagination_class = StandardResultPagination
    permission_classes = [permissions.IsAuthenticated, ]


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.IsAuthenticated, ]


class ProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductCreateSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductImageAddView(generics.CreateAPIView):
    serializer_class = ProductImageSerializer
    queryset = ProductImage.objects.all()
    permission_classes = [IsProductOwner, ]


class ProductUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsOwner, ]
    serializer_class = ProductUpdateSerializer


class ProductDeleteView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    permission_classes = [IsOwner, ]