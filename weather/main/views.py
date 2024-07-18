import urllib.parse

from django.http import JsonResponse
from django.views.generic import TemplateView
from main.forms import CityForm
from main.models import City
from main.serializers import CitySerializer
from main.utils import get_weather
from rest_framework import generics


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CityForm()
        last_city = self.request.COOKIES.get('last_city')
        if last_city:
            last_city = urllib.parse.unquote(last_city)
            context['last_city'] = last_city.capitalize()
        return context

    def post(self, request, *args, **kwargs):
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            weather = get_weather(city)
            if weather:
                data = {
                    'temperature': weather.get('temperature'),
                    'windspeed': weather.get('windspeed'),
                    'city': city.capitalize()
                }
                response = JsonResponse(data)
                # Кодируем город в безопасный для URL формат
                safe_city = urllib.parse.quote(city)
                response.set_cookie(
                    'last_city',
                    safe_city.capitalize(),
                    max_age=30*24*60*60)
                city_obj, created = City.objects.get_or_create(
                    name=city.capitalize())
                city_obj.increment_requests()
                return response
            else:
                return JsonResponse({
                    'error': f"Нет данных о погоде для {city.capitalize()}"},
                    status=404)
        else:
            return JsonResponse({
                'error': 'Неверный ввод формы'},
                status=400)


class CityListAPIView(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer
