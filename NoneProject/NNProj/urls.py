from django.urls import path
from hello import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('prime/<str:Name>', views.prime, name='Prime'),
    path('edit/<str:Name>', views.edit, name='Edit'),
    path('delete/<str:Name>', views.delete),

    path('createTask/<str:Name>', views.createTask, name='CreateTask'),
    path('deleteTask/<int:id>', views.deleteTask, name='DeleteTask'),
]