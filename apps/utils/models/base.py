from django.db.models import Model
from django.db.models import (
    BigAutoField,
    BooleanField,
    DateTimeField,
    ForeignKey,
    SET_NULL
)
from django.utils import timezone


class AbstractBaseModel(Model):
    id = BigAutoField(primary_key=True)
    created_by = ForeignKey(
        'users.User', on_delete=SET_NULL, null=True, blank=True, related_name='+'
    )
    created_at = DateTimeField(default=timezone.now)
    updated_by = ForeignKey(
        'users.User', on_delete=SET_NULL, null=True, blank=True, related_name='+'
    )
    updated_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']