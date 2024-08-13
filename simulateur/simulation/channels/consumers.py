import json
import logging

from channels.generic.websocket import AsyncWebsocketConsumer

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
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')

            if message_type == 'news':
                await self.handle_news(text_data_json)
            elif message_type == 'trigger':
                await self.handle_trigger(text_data_json)
            elif message_type == 'event':
                await self.handle_event(text_data_json)
            elif message_type == 'transaction':
                await self.handle_transaction(text_data_json)
            else:
                logger.warning(f"Unknown message type received: {message_type}")

            logger.debug(f"Message received in room {self.room_group_name}: {text_data_json}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")

    async def handle_news(self, data):
        news_message = data.get('message', 'No news message')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'news_update',
                'message': news_message
            }
        )

    async def handle_trigger(self, data):
        trigger_message = data.get('message', 'No trigger message')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'trigger_update',
                'message': trigger_message
            }
        )

    async def handle_event(self, data):
        event_message = data.get('message', 'No event message')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'event_update',
                'message': event_message
            }
        )

    async def handle_transaction(self, data):
        transaction_message = data.get('message', 'No transaction message')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'transaction_update',
                'message': transaction_message
            }
        )

    async def news_update(self, event):
        news_message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'news',
            'message': news_message
        }))
        logger.debug(f"Sent news update in room {self.room_group_name}: {news_message}")

    async def trigger_update(self, event):
        trigger_message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'trigger',
            'message': trigger_message
        }))
        logger.debug(f"Sent trigger update in room {self.room_group_name}: {trigger_message}")

    async def event_update(self, event):
        event_message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'event',
            'message': event_message
        }))
        logger.debug(f"Sent event update in room {self.room_group_name}: {event_message}")

    async def transaction_update(self, event):
        transaction_message = event['message']
        await self.send(text_data=json.dumps({
            'type': 'transaction',
            'message': transaction_message
        }))
        logger.debug(f"Sent transaction update in room {self.room_group_name}: {transaction_message}")

    async def simulation_update(self, event):
        data = event['message']
        await self.send(text_data=json.dumps(data))
        logger.debug(f"Sent simulation update in room {self.room_group_name}: {data}")
