from django.db import models


class Cell(models.Model):
    """Ячейка подстанции"""

    class Meta:
        verbose_name = "Ячейка"
        verbose_name_plural = "Ячейки"

    def __str__(self):
        return "Ячейка №{} ({})".format(self.cell, self.name)

    cell = models.IntegerField(verbose_name="Ячейка", primary_key=True)
    name = models.CharField(verbose_name='Наименование', max_length=40)
    serial_number = models.CharField(verbose_name="Номер счётчика", max_length=20)
    coeff = models.IntegerField(verbose_name="Коэффициент", default=1)

    note = models.TextField(verbose_name='Примечание', blank=True, null=True)


def get_energy_type_names():
    return [(1, "PE"), (2, "PI"), (3, "QE"), (4, "QI")]


class Profile(models.Model):
    """Получасовой профиль нагрузки"""

    class Meta:
        verbose_name = "Профиль нагрузки"
        verbose_name_plural = "Профили нагрузок"
        unique_together = ('cell', 'date', 'time', 'value_type')
        
    def __str__(self):
        return "{} {} {} {} {}".format(self.date.strftime("%d.%m.%Y"),
                                       self.time.strftime("%H:%M"),
                                       self.cell,
                                       self.value_type,
                                       self.value)
    
    ENERGY_TYPE = ((1, "Активный приём"),
                   (2, "Активная отдача"),
                   (3, "Реактивный приём"),
                   (4, "Реактивная отдача"))

    cell = models.ForeignKey("Cell", verbose_name="Ячейка", on_delete=models.SET_NULL, null=True)
    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    value_type = models.PositiveSmallIntegerField(verbose_name="Тип", choices=ENERGY_TYPE, default=1)
    value = models.CharField(verbose_name="Значение", max_length=10, blank=True, null=True)

    @property
    def energy(self):
        return "{0:.2f}".format(float(self.value) * self.cell.coeff * 0.5)


class Rept(models.Model):
    """Отчётные данные (обороты) за прошедшие сутки"""

    class Meta:
        verbose_name = "Регистр"  # ????
        verbose_name_plural = "Регистры"
        unique_together = ('date', 'time', 'name')

    REPT_TYPE = ((1, "Строка"),
                 (2, "Целое"),
                 (3, "Вещественное"),
                 (4, "JSON"),
                 (5, "XML"),)

    date = models.DateField(verbose_name="Дата")
    time = models.TimeField(verbose_name="Время")
    name = models.CharField(verbose_name="Имя", max_length=40)
    value_type = models.PositiveSmallIntegerField(verbose_name="Тип", choices=REPT_TYPE, default=1)
    value = models.CharField(verbose_name="Значение", max_length=1024, blank=True, null=True)


class Log(models.Model):
    """Логи"""
    pass
