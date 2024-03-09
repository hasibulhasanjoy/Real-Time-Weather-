from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("hourly/", views.forecastWeather, name="hourly"),
    path("daily/", views.dailyForecast, name="daily"),
]
