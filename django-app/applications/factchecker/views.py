from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .serializers import (
    SearchRequestDtoOutSerializer,
    SearchRequestDtoInSerializer,
)
from .models import SearchRequest
from applications.elasticsearch.retreiver import get_query
import asyncio
import json


def health(request):
    return HttpResponse("Server is running")


@api_view(["GET"])
def history(request):
    latest = SearchRequest.objects.all().order_by("-datetime")[:20]

    serializer = SearchRequestDtoOutSerializer(latest, many=True)

    return HttpResponse(json.dumps(serializer.data), content_type="application/json")


@api_view(["POST"])
def verify(request):
    serializer = SearchRequestDtoInSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    dto = serializer.validated_data
    method = str(dto["verification_method"])

    if method != "dpr":
        return HttpResponse("The method is not supported")
    claim = str(dto["claim"])

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(get_query(claim))
    loop.run_until_complete(future)

    results = future.result()

    dto_out = SearchRequest(claim=claim, verification_method=method)
    dto_out.save()

    for result in results:
        result.request_id = dto_out.id
        result.save()
    dto_out.answer_set.set(results)
    dto_out.save()

    response = SearchRequestDtoOutSerializer(dto_out).data

    return HttpResponse(
        json.dumps(response), content_type="application/json; charset=utf8"
    )
