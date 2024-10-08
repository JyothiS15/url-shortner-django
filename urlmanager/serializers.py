from django.core import validators
from rest_framework import serializers


class UrlSerializer(serializers.Serializer):
    """
    Serializer to validate if url is as per standards or not
    """

    url = serializers.CharField(validators=[validators.URLValidator()], max_length=1000)
