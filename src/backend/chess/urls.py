from django.urls import re_path
from rest_framework.routers import DefaultRouter

from . import views
from . import consumers


router = DefaultRouter()
router.register('matches', views.ChessMatchesViewSet, basename='chess_matches')

urlpatterns = router.urls

websocket_urlpatterns = [
    re_path(r'ws/play/(?P<game_id>\w+)/$', consumers.ChessMatchConsumer.as_asgi()),
]
