from django.urls import path, include
from hello import views
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView

urlpatterns = [
    path('create/', views.create),
    path('register/', views.registration),
    path('login/', views.login),
    path('hello/', views.hello),
    path('login/delete/<int:Id>', views.delete),
    path('hello/delete/<int:Id>', views.delete),
    path('login/edit/<int:id>', views.loginedit),
    path('hello/edit/<int:id>', views.edit),

    path('api/', include('hello.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]