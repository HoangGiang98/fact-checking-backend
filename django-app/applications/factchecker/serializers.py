from rest_framework.serializers import ModelSerializer

from .models import SearchRequest


class SearchRequestSerializer(ModelSerializer):
    class Meta:
        model = SearchRequest
        fields = ("claim", "answer", "datetime")
