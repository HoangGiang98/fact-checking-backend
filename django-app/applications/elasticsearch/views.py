from django_elasticsearch_dsl_drf.constants import (
    LOOKUP_FILTER_RANGE,
    LOOKUP_QUERY_IN,
    LOOKUP_QUERY_GT,
    LOOKUP_QUERY_GTE,
    LOOKUP_QUERY_LT,
    LOOKUP_QUERY_LTE,
)
from django_elasticsearch_dsl_drf.filter_backends import (
    FilteringFilterBackend,
    OrderingFilterBackend,
    DefaultOrderingFilterBackend,
    SearchFilterBackend,
)
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from django.http import HttpResponse

from .retreiver import get_query
import json


# from .knowledge_source import KnowledgeSourceDocument



async def handle_fact_check_by_elasticsearch(request,fact) :
    print(fact)
    result  =  await get_query(fact)
    print(result)
    return HttpResponse(result)

# class KnowledgeSourceViewSet(DocumentViewSet):
#     document = KnowledgeSourceDocument

#     lookup_field = "id"
#     filter_backends = [
#         FilteringFilterBackend,
#         OrderingFilterBackend,
#         DefaultOrderingFilterBackend,
#         SearchFilterBackend,
#     ]

#     # Define search fields
#     search_fields = (
#         "title",
#         "body",
#     )

#     # Filter fields
#     filter_fields = {
#         "id": {
#             "field": "id",
#             "lookups": [
#                 LOOKUP_FILTER_RANGE,
#                 LOOKUP_QUERY_IN,
#                 LOOKUP_QUERY_GT,
#                 LOOKUP_QUERY_GTE,
#                 LOOKUP_QUERY_LT,
#                 LOOKUP_QUERY_LTE,
#             ],
#         },
#         "title": "title.raw",
#         "body": "body.raw",
#         "created_at": "created_at",
#     }

#     # Define ordering fields
#     ordering_fields = {"id": "id", "title": "title.raw", "created": "created"}

#     # Specify default ordering
#     ordering = (
#         "id",
#         "created",
#     )
