from django.shortcuts import render


def searchCity(request):
    city = "london"
    if request.method == "POST":
        city = request.POST["city"]
    return city
