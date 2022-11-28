from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .knowledge_source import KnowledgeSourceDocument


class KnowledgeSourceDocumentSerializer(DocumentSerializer):
    class Meta:
        document = KnowledgeSourceDocument
        fields = (
            "id",
            "title",
            "body",
            "author",
            "created",
            "modified",
            "pub_date",
        )
