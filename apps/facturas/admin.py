from django.contrib import admin
from .models import Factura

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'paciente', 'total', 'estado', 'activo')
    list_filter = ('estado',)
