from django.http import HttpResponse

from rest_framework.decorators import api_view


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


@api_view(["GET", "PUT"])
def effect(request):
    if request.method == "PUT":
        pass
    if request.method == "GET":
        return HttpResponse("Return list of effects")
