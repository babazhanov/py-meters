from django.db import models


class Preference(models.Model):

    class Meta:
        verbose_name = "Настройка"
        verbose_name_plural = "Настройки"

    name = models.CharField(verbose_name="Название", max_length=80, unique=True)
    value = models.TextField(verbose_name="Значение")
