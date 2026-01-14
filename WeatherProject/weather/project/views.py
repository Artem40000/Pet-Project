from django.shortcuts import render
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry


def prime(request):
    return render(request, "prime.html")

def Moscow(request):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 55.7522,
        "longitude": 37.6156,
        "current": ["wind_speed_10m", "temperature_2m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_wind_speed_10m = current.Variables(0).Value()
    current_temperature_2m = current.Variables(1).Value()
    Data = {"Temp": round(current_temperature_2m), "Wind": round(current_wind_speed_10m, 1)}
    return render(request, "Moscow.html", {"Data": Data})


def Kazan(request):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 55.7887,
        "longitude": 49.1221,
        "current": ["wind_speed_10m", "temperature_2m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_wind_speed_10m = current.Variables(0).Value()
    current_temperature_2m = current.Variables(1).Value()
    Data = {"Temp": round(current_temperature_2m), "Wind": round(current_wind_speed_10m, 1)}
    return render(request, "Kazan.html", {"Data": Data})


def Chicago(request):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 41.85,
        "longitude": -87.65,
        "current": ["wind_speed_10m", "temperature_2m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_wind_speed_10m = current.Variables(0).Value()
    current_temperature_2m = current.Variables(1).Value()
    Data = {"Temp": round(current_temperature_2m), "Wind": round(current_wind_speed_10m, 1)}
    return render(request, "Chicago.html", {"Data": Data})


def NewYork(request):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    openmeteo = openmeteo_requests.Client(session=retry_session)
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 40.7143,
        "longitude": -74.006,
        "current": ["wind_speed_10m", "temperature_2m"],
        "wind_speed_unit": "ms",
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    current = response.Current()
    current_wind_speed_10m = current.Variables(0).Value()
    current_temperature_2m = current.Variables(1).Value()
    Data = {"Temp": round(current_temperature_2m), "Wind": round(current_wind_speed_10m, 1)}
    return render(request, "NewYork.html", {"Data": Data})