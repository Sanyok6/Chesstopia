from django.db.models import Q
from rest_framework import pagination, status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import ChessMatch
from .serializers import (ChessMatchSerializer,
                          ChessMatchCreateSerializer)


class ChessMatchesPaginator(pagination.PageNumberPagination):
    page_size = 30


class ChessMatchesViewSet(ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = ChessMatchesPaginator

    def get_queryset(self):
        user = self.request.user
        return (ChessMatch.objects.filter(Q(white=user) | Q(black=user))
                .select_related('white', 'black').order_by("-created_at"))

    def get_serializer_class(self):
        if self.action.lower() in ("create", "update", "partial_update", "delete"):
            return ChessMatchCreateSerializer

        else:
            return ChessMatchSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(ChessMatchSerializer(instance, context=self.get_serializer_context()).data,
                        status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        updated_instance = serializer.save()

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(ChessMatchSerializer(updated_instance,
                                             context=self.get_serializer_context()).data)
