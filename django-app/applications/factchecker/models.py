from django.db import models


class SearchRequest(models.Model):
    """A model representing verification requests: requested claim and the answer."""

    claim = models.CharField(max_length=30, help_text="Verification claim")
    # FIXME: adjust as soon as more decisions are made
    answer = models.CharField(max_length=30, help_text="Answer")
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.claim, self.answer)
