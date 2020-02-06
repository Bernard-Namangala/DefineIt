from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path('', views.index_view, name="home")
]

handler404 = "main.views.handler404"
