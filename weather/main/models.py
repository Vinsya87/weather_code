from django.db import models


class City(models.Model):
    name = models.CharField(
        'Название',
        max_length=100,
        unique=True)
    requests_count = models.PositiveIntegerField(
        'Количество',
        default=0)

    class Meta:
        verbose_name_plural = 'Города'
        verbose_name = 'Город'
        ordering = ['-requests_count']

    def __str__(self):
        return self.name.capitalize()

    def increment_requests(self):
        self.requests_count += 1
        self.save()
