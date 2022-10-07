from django.urls import re_path

from apps.chats.consumers import ChatsConsumer

chats_urlpatterns = [
    re_path(r'ws/chats/(?P<room>\w+)/$', ChatsConsumer.as_asgi()),
]
