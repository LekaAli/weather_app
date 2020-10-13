from django.urls import path, include
from weather import views

urlpatterns = [
    path('weather/forecast/', views.fetch_temp_readings, name='api')
]