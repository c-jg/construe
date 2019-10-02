from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Report(models.Model):
    url = models.CharField(max_length = 50)
    report_name = models.CharField(max_length = 200)
    created = models.DateTimeField(auto_now_add=True, null=True)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    keywords = ArrayField(models.CharField(max_length = 200, null=True))
    keyword_count = ArrayField(models.IntegerField(null=True))

    entities = ArrayField(models.CharField(max_length = 200, null=True))
    entity_count = ArrayField(models.IntegerField(null=True))
    
    spam = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    
    concepts = ArrayField(models.CharField(max_length = 200, null=True))
    concept_relevance = ArrayField(models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True))

    sentiment = ArrayField(models.IntegerField(null=True))    

    title = models.TextField(null=True)
    comments = models.IntegerField(null=True)
    views = models.IntegerField(null=True)

    def __str__(self):
        return self.report_name