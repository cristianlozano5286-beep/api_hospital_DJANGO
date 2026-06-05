from django.contrib import admin
from .models import Pacientes, Medicos, Citas, Especialidades, Facturas, Medicamentos, Pagos, Tratamientos

# Registra uno por uno los que quieras ver en el admin
admin.site.register(Pacientes)
admin.site.register(Medicos)
admin.site.register(Citas)
admin.site.register(Especialidades)
admin.site.register(Facturas)
admin.site.register(Medicamentos)
admin.site.register(Pagos)
admin.site.register(Tratamientos)