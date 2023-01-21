
from django.http import HttpResponse

from .retreiver import get_query
from .retreiver import get_top10


async def handle_fact_check_by_elasticsearch(request, fact):
    print(fact)
    result = await get_top10(fact)
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
