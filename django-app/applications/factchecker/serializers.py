from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import SearchRequest, Answer
class SearchRequestDtoInSerializer(ModelSerializer):
    class Meta:
        model = SearchRequest
        fields = ("claim", "verification_method")

class AnswerDtoSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ("title", "content", "url", "refuted_nli", "not_enough_info_nli", "supported_nli", "similarity_dpr")


class SearchRequestDtoOutSerializer(ModelSerializer):
    answers = AnswerDtoSerializer(source="answer_set", many=True)

    class Meta:
        model = SearchRequest
        fields = ("claim", "verification_method", "datetime", "answers", "verdict")
