from django.urls import path

from .views import homepage, application

urlpatterns = [
    path('', homepage, name='homepage'),
    path('apply/', application, name='application'),
]