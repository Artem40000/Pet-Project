from django.urls import path
from .views import ItemAdd, ItemDelete


urlpatterns = [
    path('add/', ItemAdd.as_view(), name='hello-add'),
    path('delete/<int:item_id>/', ItemDelete.as_view(), name='hello-delete'),
]