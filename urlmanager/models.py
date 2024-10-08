from django.db import models
from django_extensions.db.models import TimeStampedModel

# Create your models here.


class UrlShort(TimeStampedModel):
    actual_url = models.URLField(blank=False, null=False, unique=True)
    shortened_url = models.URLField(blank=False, null=False, unique=True)
    user = models.CharField(blank=True, null=True, max_length=100)
