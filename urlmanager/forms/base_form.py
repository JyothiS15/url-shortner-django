from django import forms


# creating a form
class UrlInputForm(forms.Form):
    """
    Url Input Form to take in url which has to be shortended
    """

    url = forms.URLField()
