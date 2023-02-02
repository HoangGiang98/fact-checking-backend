from django.db import models    
class SearchRequest(models.Model):
    """A model representing verification requests: requested claim and the answer."""

    claim = models.CharField(max_length=250, help_text="Verification claim")
    verification_method = models.CharField(
        max_length=30, help_text="Verification method", default="dpr"
    )
    datetime = models.DateTimeField(auto_now=True)
    verdict = models.CharField(
        max_length=20,
        help_text="Is the claim supportive, refuted or not enough info",
    )

    def __str__(self):
        return "{} using search method: {}".format(
            self.claim, self.verification_method
        )

class Answer(models.Model):
    """A model representing answers provided by a verification method."""

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=300, help_text="Title of an article")
    url = models.CharField(
        max_length=2000, help_text="Link of an article", default=""
    )
    content = models.CharField(
        max_length=300, help_text="Content of an article"
    )
    refuted_nli = models.IntegerField(null=True, help_text="Refuted score")
    not_enough_info_nli = models.IntegerField(
        null=True, help_text="Not enough info score"
    )
    supported_nli = models.IntegerField(null=True, help_text="Supported score")
    similarity_dpr = models.IntegerField(
        null=True, help_text="Similarity score(only for dpr)"
    )
    request = models.ForeignKey(SearchRequest, on_delete=models.CASCADE)

    def __str__(self):
        return "{}, {}: {}.".format(self.id, self.title, self.content)
