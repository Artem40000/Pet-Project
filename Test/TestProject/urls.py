from django.urls import path
from hello import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('prime/<str:Name>', views.prime, name="Prime"),
    path('delete/<str:Name>', views.delete),
    path('createTask/', views.createTask, name='AddTask'),
    path('edit/<str:Name>', views.edit, name='Edit'),
    path('deleteTask/<int:Id>_<str:Name>', views.deleteTask),
]
