from django.urls import path
from channels.routing import URLRouter
from .consumer import GetInfoConsumer

websockets = URLRouter([
    path(
        "ws/get-values", GetInfoConsumer,
        name="get-values",
    ),
])