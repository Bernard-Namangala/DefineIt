from django.shortcuts import render


def index_view(request):
    return render(request, template_name="main/index.html")


def handler404(request, exception):
    return render(request, template_name="404.html")
