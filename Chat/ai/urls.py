from django.urls import path
from hello import views

urlpatterns = [
    path('chat/', views.chat),
    path('chat/error/', views.error),
]