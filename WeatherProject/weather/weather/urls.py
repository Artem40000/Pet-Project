from django.urls import path
from project import views

urlpatterns = [
    path('', views.prime),
    path('Moscow/', views.Moscow),
    path('Kazan/', views.Kazan),
    path('Chicago/', views.Chicago),
    path('NewYork/', views.NewYork),
]
