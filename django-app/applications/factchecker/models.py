from django.db import models


class SearchRequest(models.Model):
    """A model representing verification requests: requested claim and the answer."""

    claim = models.CharField(max_length=30, help_text="Verification claim")
    verification_method = models.CharField(
        max_length=30, help_text="Verification method", default="dpr"
    )
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} with {}: {}".format(
            self.claim, self.verification_method, self.answers
        )


class Answer(models.Model):
    """A model representing answers provided by a verification method."""

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=30, help_text="Title of an article")
    content = models.CharField(
        max_length=300, help_text="Content of an article"
    )
    verdict = models.CharField(
        max_length=10, help_text="How true the claim is"
    )
    request = models.ForeignKey(SearchRequest, on_delete=models.CASCADE)

    def __str__(self):
        return "{}, {}: {}. Verdict: {}".format(
            self.id, self.title, self.content, self.verdict
        )
