from rest_framework.serializers import ModelSerializer

from .models import SearchRequest, Answer


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
