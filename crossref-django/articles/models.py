from django.db import models

# Create your models here.
from django.db import models

class Article(models.Model):
    doi = models.CharField(max_length=512, unique=True)
    title = models.TextField(null=True, blank=True)
    authors = models.JSONField(null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    peer_review = models.JSONField(null=True, blank=True)
    raw = models.JSONField(null=True, blank=True)
    retrieved_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.doi} - {self.title}"
