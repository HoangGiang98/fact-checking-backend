from django.test import TestCase

from ..serializers import (
    SearchRequestDtoInSerializer,
    SearchRequestDtoOutSerializer,
)
from .factories import SearchRequestFactory, AnswerFactory
from ..models import SearchRequest, Answer


# class SearchRequestFactoryTestCase(TestCase):
#
#     request = None
#
#     @classmethod
#     def setUpTestData(cls):
#         request = SearchRequestFactory()
#         # Set up non-modified objects used by all test methods
#         user = SearchRequest.objects.create()
#         NewsLetter.objects.create(NewsLetterID=1, Email='test@test.com', Connected=False, UserID=user)
#
#     def test_str(self):
#         """Test for string representation."""
#
#         answer1 = AnswerFactory()
#         answer2 = AnswerFactory()
#         request.answers = [answer1, answer2]
#         print(str(request))
#         self.assertEqual(
#             str(request), "{}: {}".format(request.claim, request.answer)
#         )
#

# class SearchRequestDtoInSerializerTestCase(TestCase):
#     def test_model_fields(self):
#         """Serializer data matches the SearchRequest object for each field."""
#         request = SearchRequestFactory()
#         answer1 = AnswerFactory()
#         answer2 = AnswerFactory()
#         request.answers = [answer1, answer2]
#         serializer = SearchRequestDtoInSerializer(data=request.__dict__)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         for field_name in ["claim", "verification_method"]:
#             self.assertEqual(
#                 serializer.data[field_name], getattr(request, field_name)
#             )
#
#
# class SearchRequestDtoOutSerializerTestCase(TestCase):
#     def test_model_fields(self):
#         """Serializer data matches the SearchRequest object for each field."""
#         request = SearchRequestFactory()
#         serializer = SearchRequestDtoOutSerializer(data=request.__dict__)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         for field_name in ["claim", "answers"]:
#             self.assertEqual(
#                 serializer.data[field_name], getattr(request, field_name)
#             )


class EndpointsTestCase(TestCase):
    def test_health_endpoint(self):
        """Serializer data matches the SearchRequest object for each field."""
        pass

    def test_history_endpoint(self):
        """Serializer data matches the SearchRequest object for each field."""
        pass

    def test_verify_endpoint(self):
        """Serializer data matches the SearchRequest object for each field."""
        pass
