from django.shortcuts import render
from django.http import HttpResponse
from .serializers import (
    SearchRequestDtoOutSerializer,
    SearchRequestDtoInSerializer,
    WebSearchRequestDataOutSerializer
)
from rest_framework.decorators import api_view
from applications.websearch.enums import Engines
from .models import SearchRequest, SearchResponse
from applications.websearch.web_search import WebSearch
from applications.elasticsearch.retreiver import get_query
import asyncio
import json

web_search = WebSearch()

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
    claim = str(dto["claim"])
    if method != "dpr" and method != "google" and method != "bing":
        return HttpResponse("The method is not supported")
    
    dto_out = SearchRequest(claim=claim, verification_method=method)
    dto_out.save()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    if (method == "dpr"):
        future = asyncio.ensure_future(get_query(claim))
        loop.run_until_complete(future)

        results = future.result()
        for result in results:
            result.request_id = dto_out.id
            result.save()     

        dto_out.answer_set.set(results)
        dto_out.save()

        response = SearchRequestDtoOutSerializer(dto_out).data
        
        return HttpResponse(
            json.dumps(response), content_type="application/json; charset=utf8"
        )
    if (method == "google" or method == "bing"):
        future = None
        if method == "bing":
            future = asyncio.ensure_future(web_search.fact_check_claim(claim=claim, engine= Engines.BING))
        if method == "google":
            future = asyncio.ensure_future(web_search.fact_check_claim(claim=claim, engine= Engines.GOOGLE))
        loop.run_until_complete(future)

        factcheck_result = future.result()

        factcheck_response = SearchResponse(
            claim=factcheck_result["claim"], 
            results=factcheck_result["results"],
            verdict=factcheck_result["verdict"], 
            request= dto_out
            )
        factcheck_response.save()
        dto_out.save()

        websearch_response = WebSearchRequestDataOutSerializer(dto_out).data
        
        return HttpResponse(
            json.dumps(websearch_response), content_type="application/json; charset=utf8"
        )
        

