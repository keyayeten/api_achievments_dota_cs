from django.http import HttpResponse


def status_view(request):
    return HttpResponse(status=200)
