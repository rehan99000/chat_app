import json
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatsConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        kwargs = self.scope['url_route']['kwargs']
        room_num = list(kwargs.values())[0]
        self.group_name = f'room-{room_num}'

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def websocket_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))
