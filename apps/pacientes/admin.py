from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('documento_identidad', 'apellidos', 'nombres', 'activo')
    search_fields = ('nombres', 'apellidos')
