from django.urls import path, include

from .views import home

app_name = "scheduler"
urlpatterns = [
    path('', home, name="home"),
]