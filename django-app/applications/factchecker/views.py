from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from .serializers import SearchRequestSerializer
from .models import SearchRequest


# Create your views here.


def health(request):
    return HttpResponse("Server is running")


@api_view(["GET"])
def history(request):
    latest = SearchRequest.objects.all().order_by("-datetime")[:20]

    serializer = SearchRequestSerializer(latest, many=True)

    return HttpResponse(serializer.data, content_type="application/json")


@api_view(["POST"])
def verify(request):
    serializer = SearchRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    dto = serializer.Meta.model
    print(dto.claim)
    print(dto.answer)

    return HttpResponse("Answer")
