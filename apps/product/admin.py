from django.contrib import admin

from apps.product.models import Product, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('title', 'price', 'quantity', 'stock', 'category')
    search_fields = ('title', )

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
