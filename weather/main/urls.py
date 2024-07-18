from django.urls import path
from main.views import CityListAPIView, IndexView

app_name = 'main'

urlpatterns = [
    path('api/cities/', CityListAPIView.as_view(), name='city-list'),
    path('', IndexView.as_view(), name='main_index'),
    ]
