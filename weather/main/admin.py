from django.contrib import admin

from .models import City


@admin.register(City)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('name', 'requests_count')
    search_fields = ['name']
