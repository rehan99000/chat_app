from django.db import models

from apps.users.models import User
from apps.utils.models.base import AbstractBaseModel


class Room(AbstractBaseModel):
    name = models.TextField()
    admins = models.ManyToManyField(User, blank=True, related_name='admins')
    users = models.ManyToManyField(User, blank=True, related_name='users')


class Message(AbstractBaseModel):
    """
    Materials model.
    """
    text = models.TextField(db_index=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

