from django.contrib import admin
from .models import Cell, Profile #, PE_Profile, PI_Profile, QE_Profile, QI_Profile


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ['cell', 'name', 'serial_number', 'coeff', 'note']
    ordering = ['name',]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['date', 'time', 'cell', 'value_type', 'value']
    ordering = ['date', 'time', 'cell', 'value_type']

'''
@admin.register(PE_Profile)
class PE_ProfileAdmin(admin.ModelAdmin):
    list_display = ['date', 'time', 'cell', 'pe']
    ordering = ['date', 'time', 'cell']


@admin.register(PI_Profile)
class PI_ProfileAdmin(admin.ModelAdmin):
    list_display = ['date', 'time', 'cell', 'pi']
    ordering = ['date', 'time', 'cell']


@admin.register(QE_Profile)
class QE_ProfileAdmin(admin.ModelAdmin):
    list_display = ['date', 'time', 'cell', 'qe']
    ordering = ['date', 'time', 'cell']


@admin.register(QI_Profile)
class QI_ProfileAdmin(admin.ModelAdmin):
    list_display = ['date', 'time', 'cell', 'qi']
    ordering = ['date', 'time', 'cell']
'''