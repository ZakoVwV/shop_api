from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import mixins

from apps.chat.models import Room, Message
from apps.chat.serializers import RoomSerializer, MessageSerializer


class RoomViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def history(self, request, pk=None):
        room = self.get_object()
        message = room.messages.order_by('created_at')
        page = self.paginate_queryset(message)
        if page is not None:
            serializer = MessageSerializer(message, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MessageSerializer(message, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)



class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
