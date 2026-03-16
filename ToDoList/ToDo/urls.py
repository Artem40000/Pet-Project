from django.urls import path
from hello import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('prime/<str:Name>', views.prime),
    path('create/', views.create),
    path('delete/<str:Name>', views.delete),
    path('createTask/<str:Name>', views.createTask),
]
