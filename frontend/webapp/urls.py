from django.urls import path

from .views import application

urlpatterns = [
    path('apply/', application, name='application'),
]