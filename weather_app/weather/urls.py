from django.urls import path, include
from weather import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('web-view', views.fetch_temp_readings, name='bar-chart-view'),
    path('api-view/forecast', views.WeatherViewSet.as_view(), name='api-view'),
    path('api-view/obtain-token/', obtain_jwt_token)
]