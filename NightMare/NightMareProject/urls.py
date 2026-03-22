from django.contrib import admin
from django.urls import path
from hello import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('Nightmare/', views.Nightmare),
    path('register/', views.register),
    path('login/', views.login),
    path('prime/<str:Name>', views.prime),
    path('delete/<str:Name>', views.delete),
]
