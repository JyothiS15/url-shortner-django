import traceback

from django.shortcuts import redirect, render
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND
from rest_framework.views import APIView

from urlmanager.serializers import UrlSerializer
from urlmanager.service import fetch_redirect_url, fetch_shorten_url

from .forms.base_form import UrlInputForm


class GetShortenedUrl(APIView):
    """
    Api View class to Generate Shortened URL for the valid URL shared
    """

    permission_classes = [AllowAny]

    def get(self, request):
        try:
            request_data = request.GET

            serialiser = UrlSerializer(data=request_data)
            serialiser.is_valid(raise_exception=True)

            url = request_data["url"]
            shorten_url, created = fetch_shorten_url(url)
            response = {"error_status": False, "shortened_url": shorten_url}
            if created:
                status_code = HTTP_201_CREATED
            else:
                status_code = HTTP_200_OK
        except Exception as exc:
            print(traceback.print_stack())
            print(str(exc))
            response = {"error_status": True, "message": str(exc)}
            status_code = HTTP_404_NOT_FOUND
        return Response(response, status=status_code)


def generator_view(request):
    """
    UI to generate Shortened URL, this expects valid URL in the input
    """

    context = {}
    context["form"] = UrlInputForm()
    context["message"] = None

    if request.method == "POST":
        context["form"] = UrlInputForm(request.POST)
        if context["form"].is_valid():
            url = context["form"].cleaned_data["url"]

            value, created = fetch_shorten_url(url)
            message_data = f"Shortened Url is {value} for URL {url}"
            context["message"] = message_data
        else:
            print(context["form"].errors)
            print(context["form"].is_bound)
            print("Error while generating shortened url")

    return render(request, "generateShortenUrl.html", context)


class RenderShortenedUrl(APIView):
    """
    Class to either redirect to the valid url or
    raise exception of invalid url
    """

    permission_classes = [AllowAny]

    def get(self, request, hash):
        url, intact = fetch_redirect_url(hash)

        if not intact:
            context = {"message": "Url is not supported"}

            return render(request, "errortemplate.html", context)
        return redirect(f"https://www.{url}")
