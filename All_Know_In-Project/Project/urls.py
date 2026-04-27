from django.urls import path
from ProjectApp import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login),
    path('prime/<str:Name>', views.prime, name='Prime'),

    path('account-edit/<str:Name>', views.EditAccount, name='EditAccount'),
    path('account-delete/<str:Name>', views.DeleteAccount),

    path('task-create/<str:Name>', views.CreateTask, name='CreateTask'),
    path('task-delete/<int:Id>', views.DeleteTask, name='DeleteTask'),

    path('password-create/<str:Name>', views.PasswordGenerate, name='PasswordCreate')
]