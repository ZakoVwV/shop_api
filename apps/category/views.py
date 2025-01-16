from rest_framework import permissions, viewsets

from .serializers import CategorySerializer

from .models import Category



class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser(), ]
        return [permissions.AllowAny(), ]

