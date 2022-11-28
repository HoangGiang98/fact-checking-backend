from django_elasticsearch_dsl import fields
from django_elasticsearch_dsl.documents import DocType, Document
from django_elasticsearch_dsl.registries import registry

from .models import KnowledgeSource


@registry.register_document
class KnowledgeSourceDocument(Document):
    class Index:
        name = "knowledge_sources"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = KnowledgeSource

    fields = ["title", "body", "created_at"]

    def get_queryset(self):
        return super(KnowledgeSourceDocument, self).get_queryset()
