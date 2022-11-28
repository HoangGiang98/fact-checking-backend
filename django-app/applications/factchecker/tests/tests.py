from django.test import TestCase

from applications.factchecker.serializers import SearchRequestSerializer
from applications.factchecker.tests.factories import SearchRequestFactory


class SearchRequestTestCase(TestCase):
    def test_str(self):
        """Test for string representation."""
        request = SearchRequestFactory()
        self.assertEqual(
            str(request), "{}: {}".format(request.claim, request.answer)
        )


class SearchRequestSerializerTestCase(TestCase):
    def test_model_fields(self):
        """Serializer data matches the SearchRequest object for each field."""
        request = SearchRequestFactory()
        serializer = SearchRequestSerializer(data=request.__dict__)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        for field_name in ["claim", "answer"]:
            self.assertEqual(
                serializer.data[field_name], getattr(request, field_name)
            )


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
