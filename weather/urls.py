from django.urls import path
from weather.views import get_weather, index

urlpatterns = [
    path('', index, name='index')
]