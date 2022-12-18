from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view

from .serializers import ApiSearchRequestSerializer
from .models import ApiSearchRequest


def health(request):
    return HttpResponse("ApiSearch is running")


# Create your views here.
@api_view(["GET"])
def history(request):
    latest = ApiSearchRequest.objects.all().order_by("-datetime")[:20]

    serializer = ApiSearchRequestSerializer(latest, many=True)

    return HttpResponse(serializer.data, content_type="application/json")


@api_view(["POST"])
def verify(request):
    serializer = ApiSearchRequestSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    dto = serializer.Meta.model
    print(dto.claim)
    print(dto.answer)

    return HttpResponse("Answer")
