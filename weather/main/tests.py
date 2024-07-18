import unittest

from django.test import Client, TestCase
from django.urls import reverse
from main.forms import CityForm
from main.models import City
from main.serializers import CitySerializer
from main.utils import get_coordinates_from_api, get_weather
from rest_framework import status
from rest_framework.test import APIClient


class CitySerializerTest(TestCase):
    """Тесты для проверки корректности сериализатора """
    def setUp(self):
        self.city_data = {'name': 'Москва', 'requests_count': 5}
        self.city = City.objects.create(name='Москва', requests_count=5)

    def test_city_serializer(self):
        serializer = CitySerializer(instance=self.city)
        self.assertEqual(serializer.data['name'], self.city_data['name'])
        self.assertEqual(
            serializer.data['requests_count'],
            self.city_data['requests_count'])


class IndexViewTest(TestCase):
    """
    Тесты для проверки представления IndexView.
    Включает тесты для GET и POST запросов с валидными и невалидными данными.
    """
    def setUp(self):
        self.client = Client()

    def test_index_view_get(self):
        response = self.client.get(reverse('main:main_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_index_view_post_valid_form(self):
        response = self.client.post(
            reverse('main:main_index'),
            {'city': 'Москва'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('temperature', response.json())
        self.assertIn('windspeed', response.json())

    def test_index_view_post_invalid_form(self):
        response = self.client.post(reverse('main:main_index'), {'city': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())


class CityListAPIViewTest(TestCase):
    """
    Тесты для проверки API представления CityListAPIView.
    Включает тесты для получения списка городов и проверки пустого списка
    """
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('main:city-list')
        City.objects.create(name='Москва', requests_count=10)
        City.objects.create(name='Новосибирск', requests_count=5)

    def test_city_list_api_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Проверяем количество записей

    def test_city_list_api_view_empty(self):
        City.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)  # Проверяем пустой список


class UtilsFunctionsTest(TestCase):
    """
    Тесты для проверки функций get_weather
    и get_coordinates_from_api
    """
    def test_get_weather(self):
        # Тест для функции get_weather
        weather_data = get_weather('Москва')
        self.assertIsNotNone(weather_data)
        self.assertIn('temperature', weather_data)
        self.assertIn('windspeed', weather_data)

        invalid_weather_data = get_weather('InvalidCityName')
        self.assertIsNone(invalid_weather_data)

    def test_get_coordinates_from_api(self):
        # Тест для функции get_coordinates_from_api
        lat, lon = get_coordinates_from_api('Москва')
        self.assertIsNotNone(lat)
        self.assertIsNotNone(lon)

        lat_invalid, lon_invalid = get_coordinates_from_api('InvalidCityName')
        self.assertIsNone(lat_invalid)
        self.assertIsNone(lon_invalid)


class CityFormTest(TestCase):
    """
    Тесты для проверки формы CityForm.
    Включает тесты для валидных и невалидных данных.
    """
    def test_city_form_valid(self):
        form_data = {'city': 'Москва'}
        form = CityForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_city_form_invalid(self):
        form_data = {'city': ''}
        form = CityForm(data=form_data)
        self.assertFalse(form.is_valid())


if __name__ == '__main__':
    unittest.main()
