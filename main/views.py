from django.shortcuts import render, Http404
import json
from .api import get_data
from django.http import HttpResponse


def index_view(request):
    return render(request, template_name="main/index.html")


def handler404(request, exception):
    return render(request, template_name="404.html")


def index_ajax(request):
    if request.is_ajax():
        word = request.GET['word']
        data = json.dumps(get_data(word))
        print(data)
        return HttpResponse(data, content_type="application/json")

    else:
        raise Http404
