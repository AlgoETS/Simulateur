from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/simulation/(?P<room_name>\w+)/$', consumers.SimulationConsumer.as_asgi()),
]
