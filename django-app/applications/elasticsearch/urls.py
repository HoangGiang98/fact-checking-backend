from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import handle_fact_check_by_elasticsearch

router = SimpleRouter()

urlpatterns = [
    path('<str:fact>',handle_fact_check_by_elasticsearch,name = 'showmessage')
]

# router.register("items", KnowledgeSourceViewSet, basename="item")
urlpatterns += router.urls
