from rest_framework.serializers import ModelSerializer
from .models import ApiSearchRequest


class ApiSearchRequestSerializer(ModelSerializer):
    class Meta:
        model = ApiSearchRequest
        fields = ("claim", "answer", "datetime")
