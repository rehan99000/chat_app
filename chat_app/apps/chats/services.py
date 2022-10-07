from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def broadcast_update(group_name, data, action):
    async_to_sync(get_channel_layer().group_send)(
        group_name,
        {
            'type': 'websocket.message',
            'message': {
                'message': data,
                'action': action
            }
        }
    )
