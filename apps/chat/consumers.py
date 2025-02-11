import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.contrib.auth import get_user_model

from rest_framework_simplejwt.tokens import AccessToken

from apps.chat.models import Message, Room

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.user = await self.get_user_from_token()

        if self.user:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.send_notification(
                f'Пользователь {self.user.email} присоединился к чату'
            )
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        await self.send_notification(
            f'Пользователь {self.user.email} покинул чат'
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')

        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message': message,
                'user_id': self.user.id,
                'user_email': self.user.email
            }
        )

        await self.send_notification(message)

    async def chat_notification(self, event):
        message = event['message']
        user_id = event['user_id']
        user_email = event['user_email']

        if self.user.id != user_id:
            await self.send(
                text_data=json.dumps(
                    {"message": message, "user": user_email, "notification": True},
                    ensure_ascii=False
                )
            )

    async def send_notification(self, message):
        notification_data = {
            'type': 'chat.notification',
            'message': message,
            'user_id': self.user.id,
            'user_email': self.user.email
        }

        await self.channel_layer.group_send(self.room_group_name, notification_data)

    async def send_event_to_group(self, event_message):
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": 'chat.message', "message": event_message}
        )

    @database_sync_to_async
    def get_user_from_token(self, token_str):
        try:
            token = token_str.decode('utf-8').split('=')[1]
            access_token = AccessToken(token)
            user = User.objects.get(id=access_token['user_id'])
            return user
        except Exception as e:
            return None

    @database_sync_to_async
    def save_message(self, message_text):
        if self.user:
            try:
                room = Room.objects.get(name=self.room_name)
            except Room.DoesNotExist:
                room = Room.objects.create(
                    name=self.room_name,
                    host=self.user
                )
            message = Message(room=room, text=message_text, user=self.user)
            message.save()
