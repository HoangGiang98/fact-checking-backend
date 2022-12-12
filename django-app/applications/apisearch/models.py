from django.db import models

class ApiSearchRequest(models.Model):
    """A model representing fact check requests using search api: requested claim and the answer."""

    claim = models.CharField(max_length=1000, help_text="Verification claim")
    # FIXME: adjust as soon as more decisions are made
    answer = models.CharField(max_length=3000, help_text="Answer")
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {}".format(self.claim, self.answer)
