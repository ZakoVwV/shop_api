from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('apps.account.urls')),
    path('api/category/', include('apps.category.urls')),
    path('api/product/', include('apps.product.urls')),
    path('api/order/', include('apps.order.urls')),
    path('api/review/', include('apps.review.urls')),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)