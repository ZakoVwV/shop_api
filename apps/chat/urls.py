from django.urls import path, include
from rest_framework import routers
from apps.chat.views import *

router = routers.DefaultRouter()
routers.register(r'messages', MessageViewSet)
routers.register(r'rooms', RoomViewSet)

urlpatterns = [
    path('', include(router.urls))
]
