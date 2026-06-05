from django.contrib import admin
from .models import Medicamento

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('nombre_generico', 'concentracion', 'stock', 'activo')
    search_fields = ('nombre_generico',)
