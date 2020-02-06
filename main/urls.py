from django.urls import path
from . import views

app_name = "main"
urlpatterns = [
    path('', views.index_view, name="home"),
    path('def/', views.index_ajax)
]

handler404 = "main.views.handler404"
