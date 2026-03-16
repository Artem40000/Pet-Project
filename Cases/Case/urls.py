from django.urls import path, include
from hello import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('prime/<str:Name>', views.prime),
    path('create/', views.create),
    path('register/', views.register),
    path('login/', views.login),
    path('delete/<str:Name>', views.delete),

    path('case/yeti/', views.yeti),
    path('case/cracken/', views.cracken),
    path('case/dastin/', views.dastin),



    path('api/', include('hello.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]