from django.http import HttpResponse
from applications.elasticsearch.retriever import get_top_k_docs


async def handle_fact_check_by_elasticsearch(request, fact):
    result = await get_top_k_docs(fact)
    return HttpResponse(result)
