from django.shortcuts import render
from django.http import HttpResponse
from .serializers import (
    SearchRequestDtoOutSerializer,
    SearchRequestDtoInSerializer,
)
from applications.utils.enums import Engines
from rest_framework.decorators import api_view
from applications.websearch.web_search import WebSearch
from applications.elasticsearch.elastic_search import ElasticSearch
from applications.factchecker.models import SearchRequest
import asyncio
import json

web_search = WebSearch()
elastic_search = ElasticSearch()


def health(request):
    return HttpResponse("Server is running")


@api_view(["GET"])
def history(request):
    latest = SearchRequest.objects.all().order_by("-datetime")[:5]
    serializer = SearchRequestDtoOutSerializer(latest, many=True)

    return HttpResponse(
        json.dumps(serializer.data), content_type="application/json"
    )


@api_view(["POST"])
def verify(request):

    serializer = SearchRequestDtoInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    dto = serializer.validated_data
    method = str(dto["verification_method"])
    claim = str(dto["claim"])
    dto_out = SearchRequest(claim=claim, verification_method=method)
    dto_out.save()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    if method == "dpr":
        future = asyncio.ensure_future(elastic_search.elastic_dprcheck(claim))
        loop.run_until_complete(future)

        response = process_results(dto_out, future)

        return HttpResponse(
            json.dumps(response), content_type="application/json; charset=utf8"
        )
    if method == "nli_google" or method == "nli_bing" or method == "nli_wiki":
        future = None
        if method == "nli_wiki":
            future = asyncio.ensure_future(
                elastic_search.elastic_bertcheck(claim=claim)
            )
        if method == "nli_bing":
            future = asyncio.ensure_future(
                web_search.webcheck(claim=claim, engine=Engines.BING)
            )
        if method == "nli_google":
            future = asyncio.ensure_future(
                web_search.webcheck(claim=claim, engine=Engines.GOOGLE)
            )
        loop.run_until_complete(future)

        response = process_results(dto_out, future)

        return HttpResponse(
            json.dumps(response),
            content_type="application/json; charset=utf8",
        )

    return HttpResponse("The method is not supported")


def process_results(dto_out, future):
    results = future.result()["results"]
    for result in results:
        result.request_id = dto_out.id
        result.save()
    dto_out.verdict = future.result()["verdict"]
    dto_out.answer_set.set(results)
    dto_out.save()
    response = SearchRequestDtoOutSerializer(dto_out).data
    return response
