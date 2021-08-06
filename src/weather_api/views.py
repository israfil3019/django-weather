from django.shortcuts import render
from decouple import config
import requests
from .models import City
from pprint import pprint
from django.contrib import messages
from .forms import CityForm


def index(request):
    form = CityForm(request.POST or None)
    cities = City.objects.all()
    url = config('BASE_URL')
    if form.is_valid():
        n_city = form.cleaned_data["name"]
    if not City.objects.filter(name=n_city).exists():
        r = requests.get(url.format(n_city))
        if r.status_code == 200:
            form.save()
        else:
            messages.warning(request, "City does not exists.")
    else:
        messages.warning(request, "City already exists.")

    city_data = []
    for city in cities:
        print(city)
        r = requests.get(url.format(city))
        content = r.json()
        pprint(content)
        data = {
            "city": city.name,
            "temperature": content["main"]["temp"],
            "description": content["weather"][0]["description"],
            "icon": content["weather"][0]["icon"]
        }
        city_data.append(data)
    print(city_data)
    context = {
        "form": form,
        "city_data": city_data
    }
    return render(request, "weather_api/index.html", context)
