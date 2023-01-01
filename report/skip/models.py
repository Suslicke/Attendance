from ast import arg
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
tz = timezone.get_default_timezone()


class Truancy(models.Model):
    key = models.AutoField(primary_key=True)
    group = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(verbose_name="Дата")
    
    all_people = models.IntegerField(verbose_name="Всего людей")
    absenteeism = models.IntegerField(verbose_name="Количество отсутствующих")
    num_pairs = models.IntegerField(verbose_name="Количество Пар")
    
    num_hours = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Количество Часов")
    percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Процент от общего числа")
    
    def __str__(self):
        return f'Дата: {self.date} Группа: {self.group}'
    