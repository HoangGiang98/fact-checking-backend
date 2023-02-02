import json
from django.db import models
from applications.websearch.enums import Verdicts
from django.core.exceptions import ValidationError

def result_json_validator(value):
    try:
        json_data = json.loads(value)
    except json.JSONDecodeError:
        raise ValidationError("Invalid json format")
    if not isinstance(json_data, list):
        raise ValidationError("Result field must be a list")
    for element in json_data:
        if not isinstance(element, dict):
            raise ValidationError("Element must be a dictionary")
        if "title" not in element:
            raise ValidationError("Element must have a key 'title'")
        if "content" not in element:
            raise ValidationError("Element must have a key 'title'")
        if "url" not in element:
            raise ValidationError("Element must have a key 'title'")
        if not ('score' in element and isinstance(element["score"], dict) 
            and element['score'].has_key(Verdicts.SUPPORTED.value)
            and element['score'].has_key(Verdicts.REFUTED.value)
            and element['score'].has_key(Verdicts.NEUTRAL.value)):
            raise ValidationError('Invalid key or value in the result')
    
class SearchRequest(models.Model):
    """A model representing verification requests: requested claim and the answer."""

    claim = models.CharField(max_length=30, help_text="Verification claim")
    verification_method = models.CharField(
        max_length=30, help_text="Verification method", default="dpr"
    )
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{} using search method: {}".format(
            self.claim, self.verification_method
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
    
class SearchResponse(models.Model):
    """A model representing list of results with the final verdict provided by a verification method."""

    id= models.AutoField(primary_key=True)
    claim= models.CharField(max_length=10000, help_text="Verification claim")
    results = models.JSONField(help_text= "List of results", validators=[result_json_validator], default= list)
    verdict= models.CharField(max_length=20, help_text="Is the claim supportive, refuted or not enough info")
    request = models.OneToOneField(SearchRequest, on_delete=models.CASCADE)
    
    def __str__(self):
        return "{}, {}: {}. List of results: {}".format(
            self.id, self.claim, self.verdict, self.results
        )
