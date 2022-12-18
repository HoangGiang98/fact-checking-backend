from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText, FuzzyChoice, FuzzyInteger

from ..models import SearchRequest, Answer
from datetime import datetime


class SearchRequestFactory(DjangoModelFactory):
    claim = FuzzyText(length=30)
    datetime = datetime.today()
    verification_method = FuzzyChoice(choices=["dpr", "scraping"])

    def __init__(self):
        self.answers = None

    class Meta:
        model = SearchRequest


class AnswerFactory(DjangoModelFactory):
    title = FuzzyText(length=30)
    content = FuzzyText(length=30)
    verdict = FuzzyChoice(choices=["True", "False", "Uncertain"])
    request_id = FuzzyInteger(low=1)

    class Meta:
        model = Answer
