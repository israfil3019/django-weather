from django.shortcuts import render
from decouple import config
import requests
from .models import City
from pprint import pprint

def index(request):
    cities = City.objects.all()
    url = config('BASE_URL')
    city_data = []
    for city in cities:
        print(city)
        r = requests.get(url.format(city))
        content = r.json()
        pprint(content)
        data = {
            'city': city.name,
            'temperature': content['main']['temp'],
            'description': content['weather'][0]['description'],
            'icon': content['weather'][0]['icon'],
        }
        city_data.append(data)
    print(city_data)
    context = {
        'city_data': city_data
    }
    return render(request, "weather_api/index.html", context)
