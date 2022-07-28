from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views
from . import consumers


router = DefaultRouter()
router.register('matches', views.ChessMatchesViewSet, basename='chess_matches')

urlpatterns = router.urls

websocket_urlpatterns = [
    path(r'api/ws/play/<str:game_id>/', consumers.ChessMatchConsumer.as_asgi()),
]
