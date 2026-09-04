from rest_framework import generics, permissions, viewsets

from .models import Habbit
from .pagination import HabbitPagination
from .permissions import IsOwner
from .serializers import HabbitSerializer


class HabbitViewSet(viewsets.ModelViewSet):
    serializer_class = HabbitSerializer
    pagination_class = HabbitPagination

    def get_permissions(self):
        if self.action == "list":
            return [permissions.IsAuthenticated()]

        return [
            permissions.IsAuthenticated(),
            IsOwner(),
        ]

    def get_queryset(self):
        return Habbit.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PublicHabbitListAPIView(generics.ListAPIView):
    serializer_class = HabbitSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = HabbitPagination

    def get_queryset(self):
        return Habbit.objects.filter(is_public=True)
