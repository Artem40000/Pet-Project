from hello import views
from django.urls import path
from django.contrib import admin

urlpatterns = [
    path('prime/<str:name>', views.prime),
    path('register/', views.register),
    path('login/', views.login),
    path('edit/<str:name>/<str:Id>', views.edit),
    path('delete/<str:name>/<str:Id>', views.delete),
    path('create/', views.create),
    path('admin/', admin.site.urls)
]