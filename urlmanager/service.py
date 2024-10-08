import random
import string

from django.conf import settings
from tldextract import extract

from urlmanager.models import UrlShort


def generate_shorten_url(n: str = 7) -> str:
    """
    function generates random string of length 7.
    """

    # using random.choices()
    res = "".join(
        random.choices(
            string.ascii_uppercase + string.digits + string.ascii_lowercase, k=n
        )
    )

    return res


def existence_shorten_url(shorten_url: str) -> bool:
    """
    checks if shorten url already exists in DB or not
    """

    try:
        UrlShort.objects.get(shortened_url=shorten_url)
        return True
    except UrlShort.DoesNotExist:
        return False


def fetch_shorten_url(url: str) -> str:
    """
    function to either fetch a shorten url from DB if already present
    or creates a new one and returns the value
    """

    created = False
    # generalize the domain name of the url
    domain = extract(url).domain

    # match url extensions
    domain = domain + url.split(domain)[-1]

    while domain[-1] == "/":
        domain = domain[:-1]

    # check the presence of url in the db
    try:
        entity = UrlShort.objects.get(actual_url=domain)
        shortened_url = entity.shortened_url
    except UrlShort.DoesNotExist:
        # generate the url
        shorted_url = generate_shorten_url()

        retry_times = 0

        while existence_shorten_url(shorten_url=shorted_url) and retry_times < 10:
            shorted_url = generate_shorten_url()
            retry_times += 1

        if existence_shorten_url(shorten_url=shorted_url):
            raise Exception("Please reach out to Custom Care")

        _ = UrlShort.objects.create(
            actual_url=domain,
            shortened_url=shorted_url,
        )

        print(f"new entity created for url {url}")

        shortened_url = shorted_url
        created = True

    return f"{settings.WEBSITE_NAME}/{shortened_url}", created


def fetch_redirect_url(shortened_url: str) -> str:
    """
    function to return the actual url of the shorten url
    returns:
        url, active_url

        url: actual url value
        active_url: tells us if url is present or not
    """

    redirect_url = None
    try:
        # check the presence of url in the db
        url = UrlShort.objects.get(shortened_url=shortened_url)
        active_url = True
        redirect_url = url.actual_url
    except UrlShort.DoesNotExist:
        active_url = False

    return redirect_url, active_url
