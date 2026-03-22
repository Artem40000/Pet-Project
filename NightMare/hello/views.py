from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.db import connection
from .models import Person
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)
url = "https://api.open-meteo.com/v1/forecast"



def Nightmare(request):
    return render(request, "Nightmare.html")


def register(request):
    if request.method == "POST":
        person = Person()
        person.Name = request.POST.get("Name")
        person.Password = request.POST.get("Password")
        person.ConfirmPassword = request.POST.get("ConfirmPassword")
        ValidForName = Person.objects.filter(Name=person.Name)
        if person.Name == '' or person.Password == '': return HttpResponse("<h2>Заполните поля</h2>")
        if ' ' in person.Name or ' ' in person.Password: return HttpResponse("<h2>Пробел в поле(ях)</h2>")
        if len(person.Name) < 4: return HttpResponse("<h2>Имя слишком короткое</h2>")
        if len(person.Name) > 30: return HttpResponse("<h2>Имя слишком длинное</h2>")
        if len(person.Password) > 40: return HttpResponse("<h2>Пароль слишком длинный</h2>")
        if len(person.Password) < 6: return HttpResponse("<h2>Пароль слишком короткий</h2>")
        if person.Password != person.ConfirmPassword: return HttpResponse("<h2>Пароли не совпадают</h2>")
        if not str(person.Name).isalpha(): return HttpResponse("<h2>Неккоректное имя</h2>")
        if ValidForName: return HttpResponse("<h2>Пользователь уже есть</h2>")
        else: person.save()
        return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")
    return render(request, "register.html")


def login(request):
    if request.method == "POST":
        person = Person()
        person.Name = request.POST.get("Name")
        person.Password = request.POST.get("Password")
        if person.Name == '' or person.Password == '':
            return HttpResponse("<h2>Заполните поля</h2>")

        with connection.cursor() as cursor:
            cursor.execute(f'SELECT "Name" FROM hello_Person WHERE "Name" = \'{person.Name}\'')
            PersonName = cursor.fetchone()
            if PersonName: PersonName = PersonName[0]
            else: return HttpResponse("<h2>Такого пользователя нет</h2>")

            cursor.execute(f'SELECT "Password" FROM hello_Person WHERE "Password" = \'{person.Password}\'')
            PersonPassword = cursor.fetchone()
            if PersonPassword: PersonPassword = PersonPassword[0]
            else: return HttpResponse("<h2>Неверный пароль</h2>")

            if person.Name == PersonName and person.Password == PersonPassword:
                return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")
    return render(request, "login.html")


def delete(request, Name):
    person = Person.objects.get(Name=Name)
    person.delete()
    return HttpResponseRedirect(f"http://localhost:8000/register")


def prime(request, Name):
    person = Person.objects.get(Name=Name)
    if request.method == "POST":
        person = Person()
        person.Name = request.POST.get("Name")
        person.Password = request.POST.get("Password")
        ValidForName = Person.objects.filter(Name=person.Name)
        if person.Name == '' or person.Password == '': return HttpResponse("<h2>Заполните поля</h2>")
        if ' ' in person.Name or ' ' in person.Password: return HttpResponse("<h2>Пробел в поле(ях)</h2>")
        if len(person.Name) < 4: return HttpResponse("<h2>Имя слишком короткое</h2>")
        if len(person.Name) > 30: return HttpResponse("<h2>Имя слишком длинное</h2>")
        if len(person.Password) > 40: return HttpResponse("<h2>Пароль слишком длинный</h2>")
        if len(person.Password) < 6: return HttpResponse("<h2>Пароль слишком короткий</h2>")
        if not str(person.Name).isalpha(): return HttpResponse("<h2>Неккоректное имя</h2>")
        if ValidForName:
            return HttpResponse("<h2>Пользователь уже есть</h2>")
        else:
            person.save()
        return HttpResponseRedirect(f"http://localhost:8000/prime/{person.Name}")


    params = {"latitude": 55.7522,
        "longitude": 37.6156,
        "hourly": "temperature_2m",
        "current": ["temperature_2m", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    Moscow = {"Temp":round(current_temperature_2m), "Wind":round(current_wind_speed_10m, 1)}

    params = {
        "latitude": 55.7887,
        "longitude": 49.1221,
        "hourly": "temperature_2m",
        "current": ["temperature_2m", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    Kazan = {"Temp":round(current_temperature_2m), "Wind":round(current_wind_speed_10m, 1)}

    params = {
        "latitude": 59.9386,
        "longitude": 30.3141,
        "hourly": "temperature_2m",
        "current": ["temperature_2m", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    StPeter = {"Temp":round(current_temperature_2m), "Wind":round(current_wind_speed_10m, 1)}

    params = {
        "latitude": 45.0448,
        "longitude": 38.976,
        "hourly": "temperature_2m",
        "current": ["temperature_2m", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    Krasnodar = {"Temp":round(current_temperature_2m), "Wind":round(current_wind_speed_10m, 1)}

    params = {
        "latitude": 40.7143,
        "longitude": -74.006,
        "hourly": "temperature_2m",
        "current": ["temperature_2m", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    NewYork = {"Temp": round(current_temperature_2m), "Wind": round(current_wind_speed_10m, 1)}

    params = {
        "latitude": 41.85,
        "longitude": -87.65,
        "hourly": "temperature_2m",
        "current": ["temperature_2m", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    Chicago = {"Temp": round(current_temperature_2m), "Wind": round(current_wind_speed_10m, 1)}

    params = {
        "latitude": 34.0522,
        "longitude": -118.2437,
        "hourly": "temperature_2m",
        "current": ["temperature_2m", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    LosAngeles = {"Temp": round(current_temperature_2m), "Wind": round(current_wind_speed_10m, 1)}

    params = {
        "latitude": 29.7633,
        "longitude": -95.3633,
        "hourly": "temperature_2m",
        "current": ["temperature_2m", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    Houston = {"Temp": round(current_temperature_2m), "Wind": round(current_wind_speed_10m, 1)}

    params = {
        "latitude": 29.7633,
        "longitude": -95.3633,
        "hourly": "temperature_2m",
        "current": ["temperature_2m", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    Houston = {"Temp": round(current_temperature_2m), "Wind": round(current_wind_speed_10m, 1)}

    params = {
        "latitude": 57.9303,
        "longitude": 12.5335,
        "hourly": "temperature_2m",
        "current": ["temperature_2m", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    Alingsas = {"Temp": round(current_temperature_2m), "Wind": round(current_wind_speed_10m, 1)}

    params = {
        "latitude": 59.3939,
        "longitude": 15.8388,
        "hourly": "temperature_2m",
        "current": ["temperature_2m", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    Arboga = {"Temp": round(current_temperature_2m), "Wind": round(current_wind_speed_10m, 1)}

    params = {
        "latitude": 65.8252,
        "longitude": 21.6886,
        "hourly": "temperature_2m",
        "current": ["temperature_2m", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    Boden = {"Temp": round(current_temperature_2m), "Wind": round(current_wind_speed_10m, 1)}

    params = {
        "latitude": 60.4858,
        "longitude": 15.4371,
        "hourly": "temperature_2m",
        "current": ["temperature_2m", "wind_speed_10m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_temperature_2m = current.Variables(0).Value()
    current_wind_speed_10m = current.Variables(1).Value()
    Burlenge = {"Temp": round(current_temperature_2m), "Wind": round(current_wind_speed_10m, 1)}
    return render(request, "prime.html", {"person": person, "Moscow": Moscow, "Kazan": Kazan, "St": StPeter, "Krasnodar": Krasnodar, "NewYork": NewYork, "Chicago": Chicago, "LosAngeles": LosAngeles, "Houston": Houston, "Alingsas": Alingsas, "Arboga": Arboga, "Boden": Boden, "Burlenge": Burlenge})