from chat.models import ChatGroup, Message
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.group_name = self.scope['url_route']['kwargs']['chat_code']
        self.user = self.scope['user']
        self.chat_object = await self.get_chat_object_check_is_member(self.group_name)
        if self.user.is_authenticated and self.chat_object:
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()
        else:
            await self.close()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        await self.save_message_to_db(**content)
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'send_message',
                'message': {
                    'type': 'msg',
                    'sender': self.user.username,
                    'text': content['text']
                },
                'sender_channel_name': self.channel_name
            }
        )

    async def send_message(self, event):
        if event['sender_channel_name'] != self.channel_name:
            await self.send_json(event['message'])

    async def chat_activity(self, event):
        await self.send_json(event['message'])

    @database_sync_to_async
    def get_chat_object_check_is_member(self, chat_code):
        try:
            chat_object = ChatGroup.objects.get(code__exact=chat_code)
            qs = chat_object.members.filter(user_id=self.user.id)
            return chat_object if qs.exists() else None
        except ChatGroup.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message_to_db(self, text):
        Message.objects.create(group=self.chat_object, author=self.user, text=text)
