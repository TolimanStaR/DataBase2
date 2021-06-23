from django.db import models
from django.utils.translation import gettext_lazy as _


class DataType(models.TextChoices):
    integer = 'int', _('Целое число')
    float = 'float8', _('Число с плавающей точкой')
    char = 'varchar(256)', _('Char')
    text = 'text', _('Текст')


class DataBase(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)


class Table(models.Model):
    db = models.ForeignKey(to=DataBase, related_name='tables', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)


class TableColumn(models.Model):
    table = models.ForeignKey(to=Table, related_name='columns', on_delete=models.CASCADE)
    data_type = models.TextField(choices=DataType.choices, blank=True)


class TableElement(models.Model):
    content = models.TextField(blank=True)
