# board/routing.py
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # ws/board/1/
    re_path(r'ws/board/(?P<board_id>\d+)/$', consumers.BoardConsumer.as_asgi()),
]