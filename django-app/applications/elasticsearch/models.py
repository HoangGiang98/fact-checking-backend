from django.db import models
from django.utils import timezone


class KnowledgeSource(models.Model):
    """A model representing papers, documents, etc in the database"""

    title = models.CharField(max_length=100)
    body = models.CharField(max_length=5000)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title
