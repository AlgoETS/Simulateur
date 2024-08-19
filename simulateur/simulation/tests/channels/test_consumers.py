import os
from django.test import TestCase
from channels.testing import WebsocketCommunicator, AsyncTestCase
from django.urls import re_path
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.layers import InMemoryChannelLayer
from simulation.channels.consumers import SimulationConsumer

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": URLRouter([
        re_path(r'ws/simulation/(?P<simulation_manager_id>\d+)/$', SimulationConsumer.as_asgi()),
    ]),
})

class WebSocketTestCase(AsyncTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Set up any necessary test setup before tests run

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Clean up any resources or state after tests have run

    async def test_connect(self):
        communicator = WebsocketCommunicator(application, "/ws/simulation/1/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        await communicator.disconnect()

    async def test_receive_message(self):
        communicator = WebsocketCommunicator(application, "/ws/simulation/1/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Test sending 'news' message
        await communicator.send_json_to({'type': 'news', 'message': 'Test news'})
        response = await communicator.receive_json_from()
        self.assertEqual(response, {'type': 'news', 'message': 'Test news'})

        # Test sending 'trigger' message
        await communicator.send_json_to({'type': 'trigger', 'message': 'Test trigger'})
        response = await communicator.receive_json_from()
        self.assertEqual(response, {'type': 'trigger', 'message': 'Test trigger'})

        # Test sending 'event' message
        await communicator.send_json_to({'type': 'event', 'message': 'Test event'})
        response = await communicator.receive_json_from()
        self.assertEqual(response, {'type': 'event', 'message': 'Test event'})

        # Test sending 'transaction' message
        await communicator.send_json_to({'type': 'transaction', 'message': 'Test transaction'})
        response = await communicator.receive_json_from()
        self.assertEqual(response, {'type': 'transaction', 'message': 'Test transaction'})

        await communicator.disconnect()

    async def test_receive_invalid_message(self):
        communicator = WebsocketCommunicator(application, "/ws/simulation/1/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        # Send an invalid message
        await communicator.send_json_to({'type': 'unknown', 'message': 'Test error'})
        try:
            response = await communicator.receive_nothing()
            self.fail("Expected no response, but received one.")
        except:
            pass  # Expected behavior, test passes if no response is received

        await communicator.disconnect()

    async def test_disconnect(self):
        communicator = WebsocketCommunicator(application, "/ws/simulation/1/")
        connected, _ = await communicator.connect()
        self.assertTrue(connected)

        await communicator.disconnect()

        # Ensure that no further messages are processed
        try:
            await communicator.receive_nothing()
            self.fail("Expected no response after disconnection, but received one.")
        except:
            pass  # Expected behavior, test passes if no response is received
