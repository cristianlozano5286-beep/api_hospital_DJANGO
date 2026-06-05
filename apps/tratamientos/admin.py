from django.contrib import admin
from .models import Tratamiento

@admin.register(Tratamiento)
class TratamientoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cita', 'medicamento', 'dosis', 'activo')
