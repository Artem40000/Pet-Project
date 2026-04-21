from django.urls import path
from Hello import views


urlpatterns = [
    path('', views.prime),
]
