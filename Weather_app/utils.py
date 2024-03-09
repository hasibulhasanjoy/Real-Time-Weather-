def searchCity(request):
    # city = "london"
    # if request.GET.get("city"):
    #     city = request.GET.get("city")
    if request.method == "POST":
        city = request.POST["city"]
        return city
