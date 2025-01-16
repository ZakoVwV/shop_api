from rest_framework import serializers

from apps.category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.ListSerializer(child=serializers.SerializerMethodField(), required=False)

    class Meta:
        model = Category
        fields = '__all__'

    def children(self, instance):
        children = instance.children.all()
        if children:
            return CategorySerializer(children, many=True).data
        return None

