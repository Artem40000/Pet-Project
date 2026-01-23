from django.urls import path
from hello import views

urlpatterns = [
    path('create/', views.create),
    path('register/', views.register),
    path('login/', views.login),
    path('delete/<str:name>', views.delete),
    path('edit/<str:name>', views.edit),
    path('Hello/<str:name>', views.Hello),

    path('Mymy/<str:name>', views.Mymy),

    path('Poselok/page=1/<str:name>', views.Poselok1),
    path('Poselok/page=2/<str:name>', views.Poselok2),
    path('Poselok/page=3/<str:name>', views.Poselok3),
    path('Poselok/page=4/<str:name>', views.Poselok4),

    path('Jatva/page=1/<str:name>', views.Jatva1),
    path('Jatva/page=2/<str:name>', views.Jatva2),
    path('Jatva/page=3/<str:name>', views.Jatva3),

    path('LesGrimm/page=1/<str:name>', views.LesGrimm1),
    path('LesGrimm/page=2/<str:name>', views.LesGrimm2),
    path('LesGrimm/page=3/<str:name>', views.LesGrimm3),
    path('LesGrimm/page=4/<str:name>', views.LesGrimm4),
]