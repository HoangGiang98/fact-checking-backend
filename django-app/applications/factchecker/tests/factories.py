from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyText

from ..models import SearchRequest
from datetime import datetime


class SearchRequestFactory(DjangoModelFactory):
    claim = FuzzyText(length=30)
    answer = FuzzyText(length=30)
    datetime = datetime.today()

    class Meta:
        model = SearchRequest
