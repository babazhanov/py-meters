from channels.routing import ProtocolTypeRouter, URLRouter
from station.routing import websockets

application = ProtocolTypeRouter({
    "websocket": websockets,
})