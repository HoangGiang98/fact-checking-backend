from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import SearchRequest, Answer, SearchResponse
class SearchRequestDtoInSerializer(ModelSerializer):
    class Meta:
        model = SearchRequest
        fields = ("claim", "verification_method")

class AnswerDtoSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ("title", "content", "verdict")

class SearchRequestDtoOutSerializer(ModelSerializer):
    answers = AnswerDtoSerializer(source="answer_set", many=True)

    class Meta:
        model = SearchRequest
        fields = ("claim", "verification_method", "datetime", "answers")

class WebSearchRequestDataOutSerializer(ModelSerializer):
    results = SerializerMethodField()
    verdict = SerializerMethodField()
    class Meta:
        model = SearchRequest
        fields = ("claim", "verification_method", "results", "verdict", "datetime")

    def get_results(self, obj):
        return obj.searchresponse.results
    
    def get_verdict(self, obj):
        return obj.searchresponse.verdict