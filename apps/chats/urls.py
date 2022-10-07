from rest_framework.routers import DefaultRouter

from apps.chats.views import RoomsViewset, MessageViewset


router = DefaultRouter()
router.register('messages', MessageViewset, basename='messages')
router.register('rooms', RoomsViewset, basename='rooms')
app_name = 'chats'

urlpatterns = []

urlpatterns = urlpatterns + router.urls
