from django.shortcuts import render
from decouple import config
import requests
from pprint import pprint

def index(request):
    url = config('BASE_URL')
    city = "Berlin"
    r = requests.get(url.format(city))
    content = r.json()
    pprint(content)
    print(type(content))

    return render(request, "weather_api/index.html")
