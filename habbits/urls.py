from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import HabbitViewSet, PublicHabbitListAPIView

router = DefaultRouter()
router.register(r"habbits", HabbitViewSet, basename="habbits")

urlpatterns = [
    path("public/", PublicHabbitListAPIView.as_view(), name="public-habbits"),
]

urlpatterns += router.urls
