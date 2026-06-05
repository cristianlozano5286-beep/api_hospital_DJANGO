from django.contrib import admin
from .models import Medico

@admin.register(Medico)
class MedicoAdmin(admin.ModelAdmin):
    list_display = ('numero_registro', 'apellidos', 'nombres', 'especialidad', 'activo')
    search_fields = ('nombres', 'apellidos')
