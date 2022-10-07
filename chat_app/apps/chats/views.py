from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend

from apps.chats.models import Message, Room
from apps.chats.serializers import MessageSerializer, RoomSerializer
from apps.chats.services import broadcast_update
from apps.users.permissions import (
    IsAdmin,
    IsCreator,
)
from apps.users.models import User
from apps.utils.views.base import BaseViewset, ResponseInfo


class RoomsViewset(BaseViewset):
    """
    API endpoints that manages rooms.
    """
    def get_queryset(self):
        self.get_object
        return Room.objects.filter(created_by=self.request.user)

    action_serializers = {
        'default': RoomSerializer,
    }
    action_permissions = {
        'default': [IsAuthenticated],
        'create': [IsAuthenticated],
        'destroy': [IsAuthenticated, IsAdmin | IsCreator],
    }
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_param = 'search'
    search_fields = ['name']
    filterset_fields = ['created_by']

    @action(detail=True, url_path='add-users', methods=['post'])
    def add_users(self, request, *args, **kwargs):
        user_ids = request.data.get('user_ids')
        users = User.objects.filter(id__in=user_ids)
        room = self.get_object()
        for user in users:
            room.users.add(user)

        return Response(
            status=status.HTTP_200_OK,
            data=ResponseInfo().format_response(
                data={}, status_code=status.HTTP_200_OK, message='Users {} added to room {}'.format(
                    ''.join(users.values_list())
                )
            )
        )


    @action(detail=True, url_path='remove-users', methods=['post'])
    def remove_users(self, request, *args, **kwargs):
        user_ids = request.data.get('user_ids')
        users = User.objects.filter(id__in=user_ids)
        room = self.get_object()
        for user in users:
            room.users.remove(user)


        return Response(
            status=status.HTTP_200_OK,
            data=ResponseInfo().format_response(
                data={}, status_code=status.HTTP_200_OK, message='Users {} added to room {}'.format(
                    ''.join(users.values_list())
                )
            )
        )


class MessageViewset(BaseViewset):
    """
    API endpoints that manages messages.
    """
    def get_queryset(self):
        return Message.objects.filter(created_by=self.request.user)

    action_serializers = {
        'default': MessageSerializer,
    }
    action_permissions = {
        'default': [IsAuthenticated],
        'create': [IsAuthenticated],
        'destroy': [IsAuthenticated, IsAdmin | IsCreator],
    }
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_param = 'search'
    search_fields = ['text']
    filterset_fields = ['created_by', 'room']

    def create(self, request, *args, **kwargs):
        resp = super().create(request, *args, **kwargs)
        broadcast_update(f'room-{resp.data.room}', resp.data, 'Create')
        return resp

