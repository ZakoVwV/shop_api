from rest_framework import serializers

from .models import Room, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    host = serializers.ReadOnlyField(source='host.email', read_only=True)
    last_message = serializers.SerializerMethodField()
    message = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Room
        fields = '__all__'

    def get_last_message(self, instance):
        last_message = instance.message.order_by('created_at').last()
        if last_message:
            return MessageSerializer(last_message).data
        return None