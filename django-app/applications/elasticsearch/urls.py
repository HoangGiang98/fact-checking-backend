from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import KnowledgeSourceViewSet

router = SimpleRouter()

urlpatterns = []

router.register("items", KnowledgeSourceViewSet, basename="item")
urlpatterns += router.urls
