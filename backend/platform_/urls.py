from django.urls import path
# from rest_framework.routers import DefaultRouter

from .views import ApplicationViewset

# router = DefaultRouter()
# router.register(r'v1/apply', ApplicationViewset, basename='application')


urlpatterns = [
    path('api/v1/apply/', ApplicationViewset.as_view(), name='apply')
]