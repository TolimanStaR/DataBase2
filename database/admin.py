from django.contrib import admin

from .models import *


@admin.register(DataBase)
class DataBaseAdmin(admin.ModelAdmin):
    pass


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    pass


@admin.register(TableElement)
class TableElementAdmin(admin.ModelAdmin):
    pass
