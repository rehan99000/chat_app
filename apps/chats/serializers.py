from apps.chats.models import Message, Room
from apps.utils.serializers.base import BaseSerializer


class MessageSerializer(BaseSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class RoomSerializer(BaseSerializer):
    class Meta:
        model = Room
        fields = '__all__'
