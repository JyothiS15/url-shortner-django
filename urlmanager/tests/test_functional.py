"""
#############################
# functional tests
#############################
1. Generate short URL for a valid URL input
2. Do not re-generate short URL if already generated
3. {hostname}/short_url should redirect to the original url
"""


import pytest
from django.test import RequestFactory

from urlmanager.models import UrlShort
from urlmanager.views import GetShortenedUrl


@pytest.mark.django_db(databases=["default"])
def test_generation(mocker, shortend_url):
    """
    test to generate shorten url for the given input
    test if generated shorten url matches the expected url
    test if created code matchs 201
    """
    factory = RequestFactory()
    expected_url = "http://www.gp.com/DFt3WyE"

    mocker.patch(
        "urlmanager.service.generate_shorten_url",
        return_value=shortend_url,
    )

    request = factory.get(
        "/urlmanager/shorten", query_params={"url": "http://www.google.com"}
    )

    response = GetShortenedUrl.as_view()(request)

    assert response.status_code == 201
    assert expected_url == response.data["shortened_url"]


def test_generate_shorten_url():
    """
    test the generated shorten url is of length 7
    """
    from urlmanager.service import generate_shorten_url

    generated_url = generate_shorten_url()

    assert len(generated_url) == 7


@pytest.mark.django_db(databases=["default"])
def test_re_generation_shorten_url_existing_value(mocker, shortend_url):
    """
    Testing regreneration of shorten url where the generated url is already
    present in the DB and expected to generate all 10 times
    Expected behaviour is to get a error
    """
    factory = RequestFactory()

    actual_url = "http://www.google.com"
    UrlShort.objects.create(
        actual_url=actual_url,
        shortened_url=shortend_url,
    )

    mocker.patch(
        "urlmanager.service.generate_shorten_url",
        return_value=shortend_url,
    )

    request = factory.get("/urlmanager/shorten", query_params={"url": actual_url})

    response = GetShortenedUrl.as_view()(request)

    assert response.status_code == 404


@pytest.mark.django_db(databases=["default"])
def test_re_generation_shorten_url_logic(mocker, true_existance_status):
    """
    Testing regreneration of shorten url where the generated url is already
    present in the DB for every new url generated this is all 10 times
    Expected behaviour is to get a error
    """
    factory = RequestFactory()

    mocker.patch(
        "urlmanager.service.existence_shorten_url",
        return_value=true_existance_status,
    )

    request = factory.get(
        "/urlmanager/shorten", query_params={"url": "http://www.google.com"}
    )

    response = GetShortenedUrl.as_view()(request)

    assert response.status_code == 404


@pytest.mark.django_db(databases=["default"])
def test_random_generation_shorten_url():
    """
    test to generate a random shorten url
    """
    factory = RequestFactory()

    request = factory.get(
        "/urlmanager/shorten", query_params={"url": "http://www.google.com"}
    )

    response = GetShortenedUrl.as_view()(request)

    assert response.status_code == 201
