import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer

logger = logging.getLogger(__name__)

class SimulationConsumer(AsyncWebsocketConsumer):
    connections = {}  # Dictionary to store connections

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None
        self.simulation_manager_id = None

    async def connect(self):
        try:
            self.simulation_manager_id = self.scope['url_route']['kwargs']['room_name']
            if not self.simulation_manager_id:
                logger.warning(f"Missing simulation_manager_id in URL: {self.scope['url_route']['kwargs']}")
                await self.close()
                return

            self.room_group_name = f'simulation_{self.simulation_manager_id}'

            # Register the connection
            SimulationConsumer.connections[self.channel_name] = self.room_group_name

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()
            logger.info(f"WebSocket connection established for simulation manager {self.room_group_name}")

        except Exception as e:
            logger.error(f"Error during WebSocket connection: {e}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            # Unregister the connection
            if self.channel_name in SimulationConsumer.connections:
                del SimulationConsumer.connections[self.channel_name]

            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
            logger.info(f"WebSocket connection closed with code {close_code}")

        except Exception as e:
            logger.error(f"Error during WebSocket disconnection: {e}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')

            logger.debug(f"Received message: {text_data_json}")

            message_handlers = {
                'simulation_update': self.simulation_update,
                'news': self.handle_news,
                'trigger': self.handle_trigger,
                'event': self.handle_event,
                'transaction': self.handle_transaction
            }

            handler = message_handlers.get(message_type)
            if handler:
                await handler(text_data_json)
            else:
                logger.warning(f"Unknown message type received: {message_type}")

        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
        except Exception as e:
            logger.error(f"Error handling message: {e}")

    async def handle_news(self, data):
        news_message = data.get('message', 'No news message provided')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'news_update',
                'message': news_message
            }
        )

    async def handle_trigger(self, data):
        trigger_message = data.get('message', 'No trigger message provided')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'trigger_update',
                'message': trigger_message
            }
        )

    async def handle_event(self, data):
        event_message = data.get('message', 'No event message provided')
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'event_update',
                'message': event_message
            }
        )

    async def handle_transaction(self, data):
        transaction_message = data.get('message', 'No transaction message provided')
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
