import json
from channels.generic.websocket import AsyncWebsocketConsumer
import logging

logger = logging.getLogger(__name__)

class SimulationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'simulation_{self.room_name}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        logger.debug(f"WebSocket connection established for room {self.room_group_name}")

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.debug(f"WebSocket connection closed: {close_code}")

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message', 'No message')
        logger.debug(f"Message received in room {self.room_group_name}: {message}")
        await self.send(text_data=json.dumps({
            'message': message
        }))

    async def simulation_update(self, event):
        data = event['data']
        await self.send(text_data=json.dumps(data))
        logger.debug(f"Sent simulation update in room {self.room_group_name}: {data}")
