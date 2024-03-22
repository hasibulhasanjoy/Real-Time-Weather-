import requests
from django.shortcuts import render
from .utils import searchCity
from datetime import datetime

# Create your views here.
currentWeather = None
forecastWeather = None
city = None


def home(request):
    global currentWeather, forecastWeather, city
    currentWeather, forecastWeather, city = apiCall(request)
    if currentWeather is not None:
        temp = currentWeather["main"]["temp"] - 273.15
        feelsLike = currentWeather["main"]["feels_like"] - 273.15
        minimum = currentWeather["main"]["temp_min"] - 273.15
        maximum = currentWeather["main"]["temp_max"] - 273.15
        pressure = currentWeather["main"]["pressure"]
        humidity = currentWeather["main"]["humidity"]
        wind = currentWeather["wind"]["speed"]
        timestamp = currentWeather["dt"]
        formatted_time = datetime.fromtimestamp(timestamp)
        day = formatted_time.strftime("%A")
        month = formatted_time.strftime("%B")
        time = formatted_time.strftime("%I:%M %p")
        date = formatted_time.strftime("%d")
        year = formatted_time.strftime("%Y")
        temp = round(temp, 2)
        feelsLike = round(feelsLike, 2)
        minimum = round(minimum, 2)
        maximum = round(maximum, 2)
        weather = currentWeather["weather"][0]["main"]
        icon = currentWeather["weather"][0]["icon"]
        context = {
            "day": day,
            "month": month,
            "time": time,
            "date": date,
            "year": year,
            "city": city.upper(),
            "temp": temp,
            "weather": weather,
            "feels_like": feelsLike,
            "minimum": minimum,
            "maximum": maximum,
            "humidity": humidity,
            "pressure": pressure,
            "wind": wind,
            "icon": icon,
        }
        return render(request, "Weather_app/index.html", context)
    else:
        return render(request, "Weather_app/NotFound.html")


def forecastWeather(request):
    # currentWeather, forecastWeather, city = apiCall(request)
    if forecastWeather is not None:
        daily_forecast = []
        for i in forecastWeather["list"]:
            dict = {
                "date": i["dt_txt"],
                "temp": round(i["main"]["temp"] - 273.15, 2),
                "humidity": i["main"]["humidity"],
                "weather": i["weather"][0]["main"],
                "wind": i["wind"]["speed"],
                "icon": i["weather"][0]["icon"],
            }
            daily_forecast.append(dict)

        daily_forecast.append({"city": forecastWeather["city"]["name"]})
        context = {
            "daily_forecast": daily_forecast,
            "city": city,
        }
        return render(request, "Weather_app/hourly_forecast.html", context)
    else:
        return render(request, "Weather_app/NotFound.html")


def dailyForecast(request):
    # currentWeather, forecastWeather, city = apiCall(request)
    if forecastWeather is not None:
        daily_forecast = []
        date1 = ""
        date2 = ""
        for i in forecastWeather["list"]:
            date = str(i["dt_txt"])
            date1 = date[0:10]
            if date1 != date2:
                dict = {
                    "date": date1,
                    "temp": round(i["main"]["temp"] - 273.15, 2),
                    "weather": i["weather"][0]["main"],
                    "icon": i["weather"][0]["icon"],
                }
                daily_forecast.append(dict)
            date2 = date1
        context = {
            "daily_forecast": daily_forecast,
            "city": city,
        }
        return render(request, "Weather_app/daily_forecast.html", context)
    else:
        return render(request, "Weather_app/NotFound.html")


def apiCall(request):
    api_key = "6f415fc01eb20dd86ccf0e6b6164da10"
    CITY = str(searchCity(request))
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
    COMPLETE_URL = BASE_URL + "appid=" + api_key + "&q=" + CITY
    current_weather = requests.get(COMPLETE_URL).json()
    if current_weather["cod"] == 200:
        lat = str(current_weather["coord"]["lat"])
        lon = str(current_weather["coord"]["lon"])
        FORECAST_BASE_URL = "http://api.openweathermap.org/data/2.5/forecast?"
        FORECAST_FULL_URL = (
            FORECAST_BASE_URL
            + "lat="
            + lat
            + "&"
            + "lon="
            + lon
            + "&"
            + "appid="
            + api_key
        )
        forecast_weather = requests.get(FORECAST_FULL_URL).json()
        return current_weather, forecast_weather, CITY
    else:
        return None, None, None
