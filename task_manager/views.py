from django.views.generic import TemplateView
from django.http import HttpResponse


class IndexView(TemplateView):
    template_name = 'index.html'


def test_rollbar_error(request):
    """Test view to trigger a Rollbar error for testing purposes"""
    a = None
    a.hello()  # Creating an error with an invalid line of code
    return HttpResponse("Hello, world. You're at the test error page.")