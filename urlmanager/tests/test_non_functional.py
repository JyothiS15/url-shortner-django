"""
#############################
# non-functional tests
#############################
1. Check if API endpoint takes in value with invalid URL format
2. Check if API takes in extra params, if yes, does it consume ?
3. Check if short URL is regenerated for different URL by running the function
1000 times.
4. Check if API input takes empty values and also check with giving urls of
2000 character long.
"""

import random
import string

import pytest
from django.test import RequestFactory

from urlmanager.views import GetShortenedUrl


def test_wrong_url_input():
    """
    test if it takes in value with invalid URL format
    expected to fail with 404 error
    """
    factory = RequestFactory()

    request = factory.get("/urlmanager/shorten", query_params={"url": "google.com"})

    response = GetShortenedUrl.as_view()(request)

    assert response.status_code == 404


@pytest.mark.django_db(databases=["default"])
def test_api_endpoint_with_extra_params():
    """
    Test if api takes extra params in the input.
    If it does, then does it break?
    """
    factory = RequestFactory()

    actual_url = "http://www.google.com"

    request = factory.get(
        "/urlmanager/shorten",
        query_params={"url": actual_url, "query": "Delete * from UrlShort"},
    )

    response = GetShortenedUrl.as_view()(request)

    assert response.status_code == 201


@pytest.mark.django_db(databases=["default"])
def test_api_endpoint_with_empty_url_value():
    """
    test if empty url can be sent as param of url.
    expected to fail
    """
    factory = RequestFactory()

    actual_url = ""

    request = factory.get(
        "/urlmanager/shorten",
        query_params={"url": actual_url, "query": "Delete * from UrlShort"},
    )

    response = GetShortenedUrl.as_view()(request)

    assert response.status_code == 404


@pytest.mark.django_db(databases=["default"])
def test_api_endpoint_with_max_length_url_value():
    """
    test if url length more than 1000 works or not.
    there is limit on total url length of 1000.
    expected to fail with 404 error code
    """
    factory = RequestFactory()

    actual_url = "http://www.google.com/" + "".join(
        random.choices(
            string.ascii_uppercase + string.digits + string.ascii_lowercase, k=1000
        )
    )

    request = factory.get(
        "/urlmanager/shorten",
        query_params={
            "url": actual_url,
        },
    )

    response = GetShortenedUrl.as_view()(request)

    assert response.status_code == 404


@pytest.mark.parametrize("execution_number", range(100))
@pytest.mark.django_db(databases=["default"])
def test_random_generation_shorten_url_n_times(execution_number):
    """
    test for 100 requests.
    """
    factory = RequestFactory()

    request = factory.get(
        "/urlmanager/shorten", query_params={"url": "http://www.google.com"}
    )

    response = GetShortenedUrl.as_view()(request)

    assert response.status_code == 201
