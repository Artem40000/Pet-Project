from django.urls import path
from hello import views

urlpatterns = [
    path('prime/', views.prime),
    path('Task/', views.Task),
    path('CreateTask/', views.CreateTask),
    path('delete/<int:id>', views.delete),
]