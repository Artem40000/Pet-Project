from django.urls import path
from .views import PersonDetail, PersonList, PersonDelete, PersonDeleteAll, PersonEdit, PersonRegistration

urlpatterns = [
    path('register/', PersonRegistration.as_view(), name='user-register'),
    path('user/<int:user_id>/', PersonDetail.as_view(), name='user-detail'),
    path('users/', PersonList.as_view(), name='user-list'),
    path('delete/<int:user_id>/', PersonDelete.as_view(), name='user-delete'),
    path('delete-all/', PersonDeleteAll.as_view(), name='user-delete-all'),
    path('edit/<int:user_id>/', PersonEdit.as_view(), name='user-edit'),
]